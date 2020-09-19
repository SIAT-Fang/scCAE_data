library(BiocManager)
library(splatter)
library(scater)

params <- newSplatParams()
params <- setParam(params, "nGenes", 2048)
params <- setParam(params, "batchCells", 5000)
# params <- setParam(params, "group.prob", c(0.1, 0.1, 0.1, 0.25))
# params <- setParam(params, "de.prob", 0.5)
# params <- setParam(params, "de.facLoc", 0.2)
# params <- setParam(params, "path.from", c(0, 1, 1, 3))
params <- setParam(params, "dropout.type", "experiment")
params <- setParam(params, "dropout.shape", -1)
params <- setParam(params, "dropout.mid", 2)

set.seed(1)
rand = sample(50:100, 10, replace = TRUE)
rand = rand/sum(rand)


# sim <- splatSimulatePaths(params,
#                           group.prob = rand,
#                           de.prob = 0.5, de.facLoc = 0.2,
#                           path.from = c(0, 1, 2, 3, 1, 1, 5, 7, 7, 3, 10, 10, 5, 13, 14, 4, 4, 0, 18, 18, 2, 6, 6, 14, 8),
#                           verbose = FALSE)

# sim <- splatSimulatePaths(params,
#                           group.prob = rand,
#                           de.prob = 0.5, de.facLoc = 0.2,
#                           path.from = c(0, 1, 2, 3, 1, 1, 5, 7, 7, 3),
#                           verbose = FALSE)

# sim <- splatSimulateGroups(params,
#                            group.prob = rand,
#                            verbose = FALSE)

sim <- splatSimulateGroups(params,
                           group.prob = rand,
                           verbose = FALSE)

sim.matrix <- counts(sim)
sim.gourps <- data.matrix(sim@colData)

write.csv(sim.matrix, "data.csv")
write.csv(sim.gourps, "groups.csv")

sim <- logNormCounts(sim)
sim <- runPCA(sim)
plotPCA(sim, colour_by = "Group")