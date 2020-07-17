setwd('/Volumes/OSX/Users/pichugin/Projects/Project Droplet/Data/Rosettes/')


Write2File=0

#Files to write
File2write <- "RosettesCombined.txt"
# File2writeMask <- "RosettesProcessed "

#Files to read
FileMask <- "RosettesProcessed"

## create the hearder line with X values
FileName <- paste(FileMask, 0, ".txt", sep="")
Data0 <- read.csv(FileName, header=T)
# Xmin <- Data0[1, 6]
# Xmax <- Data0[1,519]
# Xarray <- seq(Xmin, Xmax, 0.1)
Header <- as.numeric(Data0[1,])
# Header <- c(Header, -1,-1,-1, -1)
# Header <- c(Header, Xarray)


ResultArray <- Header
## Compute stuff
for(filenum in 0:9){
  print(filenum)
  
  FileName <- paste(FileMask, filenum, ".txt", sep="")
  Data0 <- read.csv(FileName, header=T)
  ResultArray <- rbind(ResultArray, Data0[2:dim(Data0)[1],])

}
write.csv(ResultArray, File2write, row.names = F, col.names = F)


