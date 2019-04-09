

library(data.table)
library(mdsr)


wineInfo <- fread(file = "D:\\GitRepos\\DS220Proj2WineReview\\winemag-data-130k-v2.csv")

wines <- wineInfo %>%
  select(variety, price, winery, taster_name, title)

wineries <- wineInfo %>%
  select(variety, winery, region_1, region_2, province, designation, country)

reviewers <- wineInfo %>%
  select(variety, winery, taster_name, taster_twitter_handle, title)

reviews <- wineInfo %>%
  select(variety, winery, taster_name, title, points, description)

write.csv(wines, file = "D:\\GitRepos\\DS220Proj2WineReview\\wines.csv")
write.csv(wineries, file = "D:\\GitRepos\\DS220Proj2WineReview\\wineries.csv")
write.csv(reviewers, file = "D:\\GitRepos\\DS220Proj2WineReview\\reviewers.csv")
write.csv(reviews, file = "D:\\GitRepos\\DS220Proj2WineReview\\reviews.csv")




