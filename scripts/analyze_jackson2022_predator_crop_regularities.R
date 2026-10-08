#!/usr/bin/env Rscript
# An EXPLORATORY, outcome-exposed external ecological interaction analysis.
# Jackson et al. 2022, J Ecol DOI 10.1111/1365-2745.13867.
# Public saved model-frame source commit:
# ee-jackson/premature-fruit-drop@7568638780b880a83a0cbd89e777104fbb14f6b9
# A known predator is recorded as 1; non-recorded predator is not proven absent.
# Higher CV seed crop variation = LESS regular crop sizes, NOT dates of flowering.
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=2L) stop("usage: analyze_jackson2022_predator_crop_regularities.R public-model-fits.rds outdir")
source_file <- args[1]
outdir <- args[2]
dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
models <- readRDS(source_file)
if(!all(c("cvseed_cs","seedpred_pres") %in% names(models)))
  stop("original published fit list missing primary predictor models")
frame <- function(k) {
  x <- tryCatch(slot(models[[k]],"frame"),error=function(e) NULL)
  if(is.null(x)) x <- attributes(models[[k]])[["frame"]]
  if(!is.data.frame(x)) stop(paste("no public fitted frame:",k))
  if(!all(c("sp4","year",k) %in% names(x)))
    stop(paste("source frame not on species/year grain:",k))
  if(anyDuplicated(x[,c("sp4","year")]))
    stop(paste("duplicate species/year in source:",k))
  x
}
observed <- function(f) {
  r <- grep("^cbind\\s*\\(abscised_seeds\\s*,\\s*viable_seeds\\s*\\)$",names(f))
  if(length(r)!=1L) stop("no exact published two-part response matrix")
  y <- f[[r]]
  if(!is.matrix(y) || ncol(y)!=2L) stop("expected two-column source response")
  if(anyNA(y) || any(y<0)) stop("invalid original published seed response")
  data.frame(abscised=as.numeric(y[,1]),viable=as.numeric(y[,2]))
}
panel <- function(key) {
  f <- frame(key)
  y <- observed(f)
  data.frame(sp4=as.character(f$sp4),year=as.character(f$year),
    abscised=y$abscised,viable=y$viable,
    trait=as.character(f[[key]]),stringsAsFactors=FALSE)
}
cv <- panel("cvseed_cs")
pred <- panel("seedpred_pres")
v <- merge(cv,pred,by=c("sp4","year"),suffixes=c("_cv","_pred"),
           all=FALSE,sort=TRUE)
if(nrow(v)<500L || any(v$abscised_cv!=v$abscised_pred) ||
   any(v$viable_cv!=v$viable_pred))
  stop("source model outcomes cannot be joined on same species/year")
v$cvseed_cs <- as.numeric(v$trait_cv)
v$predator <- as.numeric(v$trait_pred)
if(anyNA(v$cvseed_cs) || anyNA(v$predator) ||
   !identical(sort(unique(v$predator)),c(0,1)))
  stop("unexpected source predictor domains")
by_sp <- split(v,v$sp4)
species <- do.call(rbind,lapply(names(by_sp),function(s) {
  d <- by_sp[[s]]
  if(length(unique(d$cvseed_cs))!=1L ||
     length(unique(d$predator))!=1L)
    stop(paste("species-level trait varies by year:",s))
  data.frame(sp4=s,cvseed_cs=d$cvseed_cs[1],
    predator=d$predator[1],n_years=nrow(d),
    a=sum(d$abscised_cv),v=sum(d$viable_cv),
    stringsAsFactors=FALSE)
}))
row.names(species) <- NULL
species$logit_abscission <- with(species,log((a+0.5)/(v+0.5)))
species$seed_n <- with(species,a+v)
if(any(!is.finite(species$logit_abscission)) || nrow(species)<40)
  stop("insufficient aggregated species-level support")
n0 <- sum(species$predator==0);n1 <- sum(species$predator==1)
if(n0<10 || n1<10) stop("insufficient independently sampled species per group")
model_fit <- function(dat,weight=NULL) {
  if(length(unique(dat$predator))!=2) return(NULL)
  # Source CV was standardized by the original paper; keep source scale.
  if(any(tapply(dat$cvseed_cs,dat$predator,sd)<1e-10)) return(NULL)
  if(is.null(weight)) lm(logit_abscission~cvseed_cs*predator,data=dat)
  else lm(logit_abscission~cvseed_cs*predator,data=dat,weights=weight)
}
fit <- model_fit(species)
if(is.null(fit)) stop("missing predictor variation in both groups")
beta <- unname(coef(fit)[["cvseed_cs:predator"]])
cat("PUBLIC EXPLORATORY SPECIES-LEVEL INTERACTION\n")
cat(sprintf("Species=%d predator recorded=%d not recorded=%d; source-years=%d\n",
    nrow(species),n1,n0,length(unique(v$year))))
cat(sprintf("Interaction (CV x predator) log odds=%.6f\n",beta))
# Bootstrap independent SPECIES, stratified on recorded predator group.
# Source counts and same-species years are never resampled as independent seeds.
set.seed(20261008)
B <- 1000L
groups <- split(species,species$predator)
bs <- replicate(B, {
  d <- do.call(rbind,lapply(groups,function(g)
    g[sample.int(nrow(g),nrow(g),replace=TRUE),,drop=FALSE]))
  result <- tryCatch(model_fit(d),error=function(e) NULL)
  if(is.null(result)) NA_real_ else unname(coef(result)[["cvseed_cs:predator"]])
})
if(sum(is.finite(bs))<0.9*B) stop("bootstrap cannot identify interaction")
interval <- unname(quantile(bs,c(.025,.975),na.rm=TRUE))
run_model <- function(data,kind,weighted=FALSE) {
  w <- if(weighted) pmin(5,sqrt(data$seed_n/median(data$seed_n))) else NULL
  f <- model_fit(data,w)
  if(is.null(f)) return(data.frame(model=kind,n_species=nrow(data),
                                  n_pred0=sum(data$predator==0),
                                  n_pred1=sum(data$predator==1),
                                  cv_x_pred=NA_real_))
  data.frame(model=kind,n_species=nrow(data),
    n_pred0=sum(data$predator==0),n_pred1=sum(data$predator==1),
    cv_x_pred=unname(coef(f)[["cvseed_cs:predator"]]))
}
sens <- rbind(
  run_model(species,"equal_weight_primary"),
  run_model(species,"cap_sqrt_seed_count_weight",TRUE),
  run_model(subset(species,n_years>=10),"ten_plus_recorded_years"))
sens$primary_species_bootstrap_lo <- c(interval[1],NA,NA)
sens$primary_species_bootstrap_hi <- c(interval[2],NA,NA)
sens$note <- "source_model_frame_exploratory_not_independent_data_not_causal"
write.csv(sens,file.path(outdir,"crop_regularities_predator_interaction.csv"),
          row.names=FALSE,na="")
print(sens,row.names=FALSE)
# The source retained data contain only fruit-drop estimates, not true
# causes of abscission or direct parasitoid/oviposition chronology.
cat("BOTH EXPLOITATION AND ENEMY-INDUCED ABSCISSION CAN PRODUCE THE SAME INTERACTION.\n")
cat("No novel strict-H1 cluster, causal test, or prospective forecast.\n")
