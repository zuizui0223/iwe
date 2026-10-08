#!/usr/bin/env Rscript
# Jackson et al 2022 public fitted-model frame audit (non-promoting).
# Source ee-jackson/premature-fruit-drop, commit
# 7568638780b880a83a0cbd89e777104fbb14f6b9
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=2L) stop("usage: probe_jackson2022_saved_model_frames.R model-fits.rds output-dir")
input <- args[1]
outdir <- args[2]
dir.create(outdir, showWarnings=FALSE, recursive=TRUE)
models <- readRDS(input)
if(!is.list(models) || !all(c("cvseed_cs","seedpred_pres") %in% names(models)))
  stop("missing required published model objects")
get_frame <- function(model) {
  z <- tryCatch(slot(model, "frame"), error=function(e) NULL)
  if(is.null(z)) z <- attributes(model)[["frame"]]
  if(!is.data.frame(z)) return(NULL)
  z
}
get_counts <- function(f) {
  if(is.null(f)) return(NULL)
  if(all(c("abscised_seeds","viable_seeds") %in% names(f))) {
    return(data.frame(a=as.numeric(f$abscised_seeds),
                      v=as.numeric(f$viable_seeds)))
  }
  # A glmer model.frame of cbind(y1,y2) retains the response as a
  # two-column matrix in ONE field, not as y1 and y2 columns.
  matching <- grep("^cbind\\s*\\(abscised_seeds\\s*,\\s*viable_seeds\\s*\\)$",
                   names(f))
  if(length(matching)!=1L) return(NULL)
  mat <- f[[matching]]
  if(!is.matrix(mat) || ncol(mat)!=2L) return(NULL)
  data.frame(a=as.numeric(mat[,1L]),v=as.numeric(mat[,2L]))
}
frame_keys_ok <- function(f) {
  !is.null(f) && all(c("sp4","year") %in% names(f)) &&
    !anyDuplicated(f[,c("sp4","year")])
}
summary_rows <- lapply(names(models), function(key) {
  f <- get_frame(models[[key]])
  keyok <- frame_keys_ok(f)
  data.frame(name=key,has_frame=!is.null(f),
    rows=if(!is.null(f)) nrow(f) else NA_integer_,
    species=if(keyok) length(unique(f$sp4)) else NA_integer_,
    years=if(keyok) length(unique(f$year)) else NA_integer_,
    has_bivariate_response=!is.null(get_counts(f)),
    has_predictor=!is.null(f) && key %in% names(f),
    duplicate_species_year=if(!is.null(f) && all(c("sp4","year") %in% names(f)))
      anyDuplicated(f[,c("sp4","year")])>0 else NA,
    stringsAsFactors=FALSE)
})
report <- do.call(rbind,summary_rows)
write.csv(report,file.path(outdir,"model_frame_availability.csv"),
          row.names=FALSE,na="")
cat("PUBLIC SAVED MODEL-FRAME AUDIT\n")
print(report,row.names=FALSE)
cv <- get_frame(models[["cvseed_cs"]])
pr <- get_frame(models[["seedpred_pres"]])
ready <- frame_keys_ok(cv) && frame_keys_ok(pr) &&
  "cvseed_cs" %in% names(cv) && "seedpred_pres" %in% names(pr) &&
  !is.null(get_counts(cv)) && !is.null(get_counts(pr))
if(ready) {
  cc <- get_counts(cv)
  pc <- get_counts(pr)
  left <- data.frame(sp4=as.character(cv$sp4),
    year=as.character(cv$year),
    a_cv=cc$a, v_cv=cc$v, cvseed_cs=as.numeric(cv$cvseed_cs))
  right <- data.frame(sp4=as.character(pr$sp4),
    year=as.character(pr$year),
    a_pr=pc$a, v_pr=pc$v,
    seedpred_pres=as.character(pr$seedpred_pres))
  joined <- merge(left,right,by=c("sp4","year"),all=FALSE)
  shared_outcome <- nrow(joined)>0L &&
    all(is.finite(joined$a_cv)) && all(is.finite(joined$v_cv)) &&
    all(is.finite(joined$a_pr)) && all(is.finite(joined$v_pr)) &&
    all(joined$a_cv==joined$a_pr) && all(joined$v_cv==joined$v_pr)
  groups <- sort(unique(joined$seedpred_pres))
  by_species <- split(joined,joined$sp4)
  n_pred0 <- sum(vapply(by_species,function(z) all(z$seedpred_pres=="0"),logical(1)))
  n_pred1 <- sum(vapply(by_species,function(z) all(z$seedpred_pres=="1"),logical(1)))
  species_constant <- all(vapply(by_species,function(z)
    length(unique(z$cvseed_cs))==1L && length(unique(z$seedpred_pres))==1L,
    logical(1)))
  summary <- data.frame(
    same_species_year_outcomes_match=shared_outcome,
    n_matched_species_year=nrow(joined),
    n_matched_species=length(unique(joined$sp4)),
    n_years=length(unique(joined$year)),
    observed_predator_levels=paste(groups,collapse=";"),
    predator_present_species=n_pred1,
    predator_not_recorded_species=n_pred0,
    species_traits_constant_across_years=species_constant,
    negative_seed_counts=any(joined$a_cv<0|joined$v_cv<0),
    analysis_source_join_ready=shared_outcome &&
      identical(groups,c("0","1")) && species_constant &&
      n_pred0>=10 && n_pred1>=10,
    status="public_saved_model_frames_not_independent_raw_release"
  )
  write.csv(summary,file.path(outdir,"reconstruction_readiness.csv"),
            row.names=FALSE)
  cat("MATCHED MODEL FRAME\n")
  print(summary,row.names=FALSE)
} else {
  writeLines("required source response matrix/keys absent",
    file.path(outdir,"reconstruction_blocker.txt"))
}
cat("No effects promoted, no independent source validation claimed.\n")
