

library(data.table)
library(mdsr)


wineInfo <- fread(file = "D:\\GitRepos\\DS220Proj2WineReview\\winemag-data-130k-v2.csv")
wineInfo <- wineInfo[1:10000,]
wineInfo[taster_name %in% c(""),10] <- "Unknown"

wines <- wineInfo %>%
  select(variety, price, winery, taster_name, title)
wines <- wines[!duplicated(wines[,c('variety', 'price')])]

wineries <- wineInfo %>%
  select(variety, winery, region_1, region_2, province, designation, country)
wineries <- wineries[!duplicated(wineries$winery)]

reviewers <- wineInfo %>%
  select(variety, winery, taster_name, taster_twitter_handle, title)
reviewers <- reviewers[!duplicated(reviewers$taster_name),]

write.csv(wines, file = "D:\\GitRepos\\DS220Proj2WineReview\\winesImport.csv")
write.csv(wineries, file = "D:\\GitRepos\\DS220Proj2WineReview\\wineriesImport.csv")
write.csv(reviewers, file = "D:\\GitRepos\\DS220Proj2WineReview\\reviewersImport.csv")
write.csv(wineInfo, file = "D:\\GitRepos\\DS220Proj2WineReview\\reviewsImport.csv")
