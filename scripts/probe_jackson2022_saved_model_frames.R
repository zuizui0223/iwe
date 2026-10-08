#!/usr/bin/env Rscript
# Non-promoting public model-object provenance probe.
# Source: Jackson et al. 2022, DOI 10.1111/1365-2745.13867
# Public research compendium: ee-jackson/premature-fruit-drop
# Pinned public Git revision: 7568638780b880a83a0cbd89e777104fbb14f6b9
# This only inspects *fitted model frames*; no original Dryad source asserted.
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=2L) stop("usage: probe_jackson2022_saved_model_frames.R model-fits.rds output-dir")
input <- args[1]
outdir <- args[2]
dir.create(outdir, showWarnings=FALSE, recursive=TRUE)
models <- readRDS(input)
if(!is.list(models) || !all(c("cvseed_cs","seedpred_pres") %in% names(models))) {
  stop("expected published named cvseed_cs and seedpred_pres model objects")
}
get_frame <- function(model) {
  z <- tryCatch(slot(model, "frame"), error=function(e) NULL)
  if(is.null(z)) z <- attributes(model)[["frame"]]
  if(!is.data.frame(z)) return(NULL)
  z
}
checks <- lapply(names(models), function(key) {
  f <- get_frame(models[[key]])
  if(is.null(f)) {
    return(data.frame(name=key,has_frame=FALSE,rows=NA_integer_,
      species=NA_integer_,years=NA_integer_,has_counts=FALSE,
      has_predictor=FALSE,duplicate_species_year=NA,stringsAsFactors=FALSE))
  }
  keycols <- all(c("sp4","year") %in% names(f))
  counts <- all(c("abscised_seeds","viable_seeds") %in% names(f))
  duplicates <- if(keycols) any(duplicated(f[,c("sp4","year")])) else NA
  data.frame(name=key,has_frame=TRUE,rows=nrow(f),
    species=if(keycols) length(unique(f$sp4)) else NA_integer_,
    years=if(keycols) length(unique(f$year)) else NA_integer_,
    has_counts=counts,has_predictor=key %in% names(f),
    duplicate_species_year=duplicates,stringsAsFactors=FALSE)
})
report <- do.call(rbind, checks)
write.csv(report,file.path(outdir,"model_frame_availability.csv"),
          row.names=FALSE,na="")
cat("PUBLIC SAVED MODEL-FRAME AUDIT\n")
print(report,row.names=FALSE)
cv <- get_frame(models[["cvseed_cs"]])
pr <- get_frame(models[["seedpred_pres"]])
ready <- !is.null(cv) && !is.null(pr) &&
 all(c("sp4","year","abscised_seeds","viable_seeds","cvseed_cs") %in% names(cv)) &&
 all(c("sp4","year","abscised_seeds","viable_seeds","seedpred_pres") %in% names(pr)) &&
 !anyDuplicated(cv[,c("sp4","year")]) &&
 !anyDuplicated(pr[,c("sp4","year")])
if(ready) {
  # The predictor models were fit separately, so never row-bind their
  # sample sizes or assert identical case inclusion.
  left <- data.frame(sp4=as.character(cv$sp4),year=as.character(cv$year),
    a_cv=as.numeric(cv$abscised_seeds),v_cv=as.numeric(cv$viable_seeds),
    cvseed_cs=as.numeric(cv$cvseed_cs))
  right <- data.frame(sp4=as.character(pr$sp4),year=as.character(pr$year),
    a_pr=as.numeric(pr$abscised_seeds),v_pr=as.numeric(pr$viable_seeds),
    seedpred_pres=as.character(pr$seedpred_pres))
  joined <- merge(left,right,by=c("sp4","year"),all=FALSE)
  shared_outcome <- with(joined,all(abs(a_cv-a_pr)<1e-7) &&
    all(abs(v_cv-v_pr)<1e-7))
  levels_ok <- length(unique(joined$seedpred_pres))==2
  summary <- data.frame(
    compatible_same_species_year=shared_outcome,
    n_matched_species_year=nrow(joined),
    n_matched_species=length(unique(joined$sp4)),
    n_years=length(unique(joined$year)),
    predator_levels=length(unique(joined$seedpred_pres)),
    two_predator_groups=levels_ok,
    analysis_admissible=shared_outcome && levels_ok &&
      length(unique(joined$sp4))>=30,
    # Provenance caveat: the model frames were fit on original data,
    # but cannot provide predation chronology or true abortion cause.
    status="public_published_fitted_model_frame_only"
  )
  write.csv(summary,file.path(outdir,"reconstruction_readiness.csv"),
            row.names=FALSE)
  cat("MATCHED MODEL FRAME\n")
  print(summary,row.names=FALSE)
} else {
  writeLines("original model frames missing required same-unit variables",
    file.path(outdir,"reconstruction_blocker.txt"))
}
cat("NOT a new strict H1 effect or a causal timing validation.\n")
