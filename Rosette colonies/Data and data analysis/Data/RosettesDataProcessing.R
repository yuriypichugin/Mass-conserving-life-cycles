setwd('/Volumes/OSX/Users/pichugin/Projects/Project Droplet/Data/Rosettes/')


Write2File=0

#Files to write
File2write <- "RosettesProcessed.txt"
File2writeMask <- "RosettesProcessed"

#Files to read
FileMask <- "RosettesLC"

## create the hearder line with X values
FileName <- paste(FileMask, 0, ".txt", sep="")
Data0 <- read.csv(FileName, header=F)
Xmin <- Data0[1, 6]
Xmax <- Data0[1,519]
Xarray <- seq(Xmin, Xmax, 0.1)
Header <- array(numeric())
Header <- c(Header, -1,-1,-1, -1)
Header <- c(Header, Xarray)



## Compute stuff
for(filenum in 0:9){
  print(filenum)
  ResultArray <- Header
  FileName <- paste(FileMask, filenum, ".txt", sep="")
  Data0 <- read.csv(FileName, header=F)
  
  for(lines in 1:dim(Data0)[1]){
    Xseq <- Data0[lines,6:520]
    Yseq <- Data0[lines,521:1035]
    Yarray <- approx(as.numeric(Xseq), as.numeric(Yseq), Xarray, method="linear")
    Newline <- c(as.numeric(Data0[lines, 1:4]), Yarray$y)
    ResultArray <- rbind(ResultArray, Newline)
  }
  File2write <- paste(File2writeMask, filenum, ".txt", sep="")
  write.csv(ResultArray, File2write, row.names = F, col.names = F)
}

# plot(as.numeric(Xseq), as.numeric(Yseq))
# lines(Yarray$x, Yarray$y)



# Off1 <- Data0[,2]
# Off2 <- Data0[,3]
# 
# MinOff <- pmin(Off1, Off2)
# MaxOff <- pmax(Off1, Off2)
# 
# Asym <- (MinOff - 1)/(MaxOff + MinOff - 2)
# ParSize <- MaxOff + MinOff
# 
# PShist <- hist(ParSize)
# AShist <- hist(Asym)
# 
# print(AShist$counts)
# print(PShist$counts)
# 
# plot(Asym, ParSize, ylim =c(19.5, 21.5))
# 
# inds <- which(Asym < 0.2)
# DataA <- Data0[inds,]
# Xes <- DataA[,6:520]
# Yes <- DataA[, 521:1035]
# plot(as.numeric(Xes[1,]),as.numeric(Yes[1,]), type="l", xlim=c(1, 21))
# for(i in 1:50){
#   lines(as.numeric(Xes[i,]),as.numeric(Yes[i,]))
# }
# title("High Asym, full")
# 
# inds <- which(Asym < 0.2)
# DataA <- Data0[inds,]
# Xes <- DataA[,6:520]
# Yes <- DataA[, 521:1035]
# plot(as.numeric(Xes[1,]),as.numeric(Yes[1,]), type="l", xlim=c(20, 21))
# for(i in 1:50){
#   lines(as.numeric(Xes[i,]),as.numeric(Yes[i,]))
# }
# title("High Asym, decay")
# 
# 
# inds <- which(ParSize > 20.9)
# DataA <- Data0[inds,]
# Xes <- DataA[,6:520]
# Yes <- DataA[, 521:1035]
# plot(as.numeric(Xes[1,]),as.numeric(Yes[1,]), type="l", xlim=c(20, 21))
# for(i in 1:50){
#   lines(as.numeric(Xes[i,]),as.numeric(Yes[i,]))
# }
# title("Large parent, decay")
# 
# inds <- which(ParSize <19)
# DataA <- Data0[inds,]
# Xes <- DataA[,6:520]
# Yes <- DataA[, 521:1035]
# plot(as.numeric(Xes[1,]),as.numeric(Yes[1,]), type="l", xlim=c(1, 21))
# for(i in 1:50){
#   lines(as.numeric(Xes[i,]),as.numeric(Yes[i,]))
# }
# title("Small parent, full")

