#!/usr/bin/env Rscript
# Pinned WCVP-v13 geography for frozen 11 plus 3 egg-receiving species.
# Eggs do not prove successful larval resources or any causal response.
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 3L) {
  stop("usage: Rscript build_ambio_host_portfolio_wcvp.R <wcvp_repo> <frozen_hosts.csv> <output_dir>")
}
wcvp_dir <- args[[1]]
frozen_path <- args[[2]]
out_dir <- args[[3]]
dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)
e <- new.env(parent=emptyenv())
load(file.path(wcvp_dir, "data", "wcvp_names.rda"), envir=e)
load(file.path(wcvp_dir, "data", "wcvp_distributions.rda"), envir=e)
stopifnot(exists("wcvp_names", envir=e), exists("wcvp_distributions", envir=e))
n <- get("wcvp_names", envir=e)
d <- get("wcvp_distributions", envir=e)
req_names <- c("plant_name_id", "taxon_rank", "taxon_status", "taxon_name", "accepted_plant_name_id")
req_dist <- c("plant_name_id", "area_code_l3", "introduced", "extinct", "location_doubtful")
stopifnot(all(req_names %in% names(n)), all(req_dist %in% names(d)))
frozen <- read.csv(frozen_path, stringsAsFactors=FALSE, check.names=FALSE)
stopifnot(all(c("accepted_plant_name_id", "accepted_name", "native_host_units", "contemporary_host_units") %in% names(frozen)))
if (nrow(frozen) != 11L || anyDuplicated(frozen$accepted_plant_name_id)) {
  stop("Frozen Anthocharis host source must have exactly 11 accepted IDs")
}
frozen$accepted_plant_name_id <- trimws(as.character(frozen$accepted_plant_name_id))
frozen$accepted_name <- trimws(as.character(frozen$accepted_name))
n$plant_name_id <- as.character(n$plant_name_id)
n$accepted_plant_name_id <- as.character(n$accepted_plant_name_id)
n$taxon_name <- as.character(n$taxon_name)
id_to_name <- setNames(n$taxon_name, n$plant_name_id)
frozen_rebuilt_names <- unname(id_to_name[frozen$accepted_plant_name_id])
if (any(is.na(frozen_rebuilt_names)) || any(frozen_rebuilt_names != frozen$accepted_name)) {
  stop("Frozen chocho accepted plant ID/name disagrees with pinned WCVP")
}

candidate_names <- c("Arabis hirsuta", "Arabidopsis thaliana", "Noccaea caerulescens")
candidate_ids <- vapply(candidate_names, function(name) {
  x <- n[
    tolower(trimws(as.character(n$taxon_rank))) == "species" &
    n$taxon_name == name, , drop=FALSE
  ]
  if (nrow(x) < 1L) stop(paste("Pinned WCVP v13 exact species missing:", name))
  # Some original name strings occur in synonym/homonym records whose
  # accepted IDs differ. The authoritative record is the unique species
  # entry whose own WCVP taxon_status is Accepted. Never pool IDs across
  # alternative homonyms merely because the displayed binomial matches.
  is_accepted <- tolower(trimws(as.character(x$taxon_status))) == "accepted"
  accepted_rows <- x[!is.na(is_accepted) & is_accepted, , drop=FALSE]
  ids <- sort(unique(as.character(accepted_rows$plant_name_id)))
  ids <- ids[!is.na(ids) & nzchar(ids)]
  cat("NAME_RESOLUTION ", name,
      " exact_name_rows=", nrow(x),
      " accepted_species_rows=", nrow(accepted_rows),
      " accepted_ids=", paste(ids, collapse=";"), "\n", sep="")
  if (length(ids) != 1L || nrow(accepted_rows) != 1L) {
    stop(paste("Pinned WCVP v13 lacks exactly one authoritative accepted species row:", name))
  }
  accepted_name <- unname(id_to_name[ids])
  if (length(accepted_name) != 1L || is.na(accepted_name) || accepted_name != name) {
    stop(paste("Pinned WCVP v13 canonical name differs:", name,
               "found:", paste(accepted_name, collapse=";")))
  }
  ids[[1]]
}, character(1))
if (anyDuplicated(candidate_ids) || any(candidate_ids %in% frozen$accepted_plant_name_id)) {
  stop("Candidate species duplicate source accepted IDs or frozen IDs")
}
target <- data.frame(
  accepted_plant_name_id=c(frozen$accepted_plant_name_id, unname(candidate_ids)),
  accepted_name=c(frozen$accepted_name, candidate_names),
  source_role=c(rep("frozen_host", nrow(frozen)),
                rep("observed_egg_candidate_not_confirmed_larval_viability", length(candidate_ids))),
  stringsAsFactors=FALSE
)
d$plant_name_id <- as.character(d$plant_name_id)
d$area_code_l3 <- as.character(d$area_code_l3)
present <- !is.na(d$area_code_l3) & nzchar(d$area_code_l3) &
  d$plant_name_id %in% target$accepted_plant_name_id &
  as.integer(d$extinct) == 0L & as.integer(d$location_doubtful) == 0L
present[is.na(present)] <- FALSE
all <- unique(d[present, c("plant_name_id", "area_code_l3", "introduced"), drop=FALSE])
all$introduced <- as.integer(all$introduced)
output <- list()
for (i in seq_len(nrow(target))) {
  host <- target[i, , drop=FALSE]
  sub <- all[all$plant_name_id == host$accepted_plant_name_id, , drop=FALSE]
  contemporary <- sort(unique(sub$area_code_l3))
  native <- sort(unique(sub$area_code_l3[
    !is.na(sub$introduced) & sub$introduced == 0L
  ]))
  if (length(contemporary) == 0L) {
    stop(paste("Pinned WCVP v13 lacks extant distribution:", host$accepted_name))
  }
  if (!all(native %in% contemporary)) stop("Native subset rule broken")
  output[[i]] <- data.frame(
    accepted_plant_name_id=host$accepted_plant_name_id,
    accepted_name=host$accepted_name,
    source_role=host$source_role,
    area_code_l3=contemporary,
    native_present=contemporary %in% native,
    contemporary_present=TRUE,
    stringsAsFactors=FALSE
  )
  if (host$source_role == "frozen_host") {
    expected <- frozen[
      frozen$accepted_plant_name_id == host$accepted_plant_name_id, , drop=FALSE
    ]
    if (length(native) != as.integer(expected$native_host_units) ||
        length(contemporary) != as.integer(expected$contemporary_host_units)) {
      stop(paste("Individual frozen host count drift:", host$accepted_name,
                 "native", length(native), "current", length(contemporary)))
    }
  }
}
presence <- do.call(rbind, output)
presence <- presence[order(presence$accepted_name, presence$area_code_l3), ]
write.csv(presence, file.path(out_dir, "host_region_presence.csv"), row.names=FALSE, na="")
write.csv(target, file.path(out_dir, "source_taxon_resolution.csv"), row.names=FALSE, na="")
baseline <- presence[presence$source_role == "frozen_host", , drop=FALSE]
base_native <- unique(baseline$area_code_l3[baseline$native_present])
base_contemporary <- unique(baseline$area_code_l3[baseline$contemporary_present])
if (!identical(c(length(base_native), length(base_contemporary),
                 length(setdiff(base_contemporary, base_native))),
               c(162L, 272L, 110L))) {
  stop("Frozen 162/272/110 geography failed source reconstruction")
}
cat("BASELINE 11 hosts native=", length(base_native),
    " current=", length(base_contemporary),
    " new=", length(setdiff(base_contemporary, base_native)), "\n", sep="")
for (name in candidate_names) {
  sub <- presence[presence$accepted_name == name, , drop=FALSE]
  cat("CANDIDATE ", name, " ID=", unique(sub$accepted_plant_name_id),
      " native=", sum(sub$native_present),
      " current=", nrow(sub), "\n", sep="")
}
