// This flow visits a GitHub page, reads some info from the page and makes a download

// Visit the webpage
https://www.insee.fr/fr/information/4769950

click //*[@id="consulter"]/div/div[4]/a
click //*[@id="consulter"]/div/div[5]/a
click //*[@id="consulter"]/div/div[6]/a
click //*[@id="consulter"]/div/div[7]/a
click //*[@id="consulter"]/div/div[8]/a

// Visit the webpage
https://www.insee.fr/fr/information/4190491

click //*[@id="consulter"]/div/div[5]/a
click //*[@id="consulter"]/div/div[7]/a
click //*[@id="consulter"]/div/div[8]/a
click //*[@id="consulter"]/div/div[9]/a

// Wait 15 seconds to give the download time to complete on slow networks 
wait 600


