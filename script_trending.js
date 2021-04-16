//const { inherits } = require("node:util")

//URLs for REST api calls
const theUrl = "http://localhost:5000/influencers"
var theCurrentFollowsUrl = "http://localhost:5000/follows?name="
var handleSearchUrl = "http://localhost:5000/handlesearch?handle="
var trendingUrl = "http://localhost:5000/trending?hours="



window.onload = function() {



  //Listen to changes in dropdown menu and fetch follows by selected twitter user when selected
  document.getElementById("gettrending").addEventListener("click", function(){
    trendingUrlTemp = trendingUrl
    trendingUrlTemp = trendingUrl + 8
    var fetchTrending = fetch(trendingUrlTemp)
    fetchTrending.then(response => {
      response.json().then(data => {
        while (document.getElementById("trendingresults").hasChildNodes()){
          document.getElementById("trendingresults").removeChild(document.getElementById("trendingresults").lastChild)
        }

        Object.entries(data.data).forEach(([key,value]) => {
          console.log(`${key}${value}`);
          var a = document.createElement('a')
          var link = document.createTextNode("@"+key);
          var text = document.createTextNode(" was followed by "+value+" influencers in the past 8 hours")
          a.appendChild(link)
          a.title = "@"+key
          a.href = "http://www.twitter.com/"+key
          var newLink = document.createElement("a")
          a.setAttribute("id", "follows")
          document.getElementById("trendingresults").appendChild(a)
          document.getElementById("trendingresults").appendChild(text)
          document.getElementById("trendingresults").appendChild(document.createElement("br"))
        })
      })
    }
    );



})
}



function getTimestampString(timestamp) {
  timestamp = Number(timestamp)*1000
  var date = new Date(timestamp)
  
  return date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getFullYear()+" "+date.getHours()+":"+date.getMinutes()+" UTC +3"
}