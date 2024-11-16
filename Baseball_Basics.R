install.packages("baseballr")
library(baseballr)
#devtools::install_github(repo = "BillPetti/baseballr")

#Testing 
bref_standings_on_date("2024-08-01", "AL Central", from = FALSE)


#For loop?

liam <- statcast_search(start_date = "2022-04-06",
                        end_date = "2022-08-01", 
                        playerid = NULL,
                        player_type = 'pitcher')

print(liam)

statcast_leaderboards(leaderboard = "exit_velocity_barrels", year = 2021)

#Getting multiple statcast searches to run
#Both starting and relief pitchers
mlb_id_surgery = c(521230,663556,664062,686753,622780,645261)
data_list <- list()
#pitching_data = numeric(6)
for(i in length(mlb_id_surgery)){
  id_insert = mlb_id_surgery[i]
  data_list[[i]] <- statcast_search(start_date = "2023-04-06",
                          end_date = "2023-08-01", 
                          playerid = id_insert,
                          player_type = 'pitcher')
}
 
 
#Working example in use here
data_list <- vector("list", length(mlb_id_surgery))
for (i in seq_along(mlb_id_surgery)) {
  id_insert <- mlb_id_surgery[i]
  data_list[[i]] <- statcast_search(start_date = "2023-04-06",
                                    end_date = "2023-08-01", 
                                    playerid = id_insert,
                                    player_type = 'pitcher')
}


devtools::install_github(repo = "BillPetti/baseballr")

