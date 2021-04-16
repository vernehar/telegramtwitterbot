//const { inherits } = require("node:util")

//URLs for REST api calls
const theUrl = "http://localhost:5000/influencers"
var theCurrentFollowsUrl = "http://localhost:5000/follows?name="
var handleSearchUrl = "http://localhost:5000/handlesearch?handle="

const fetchInfluencers = fetch(theUrl)

//Make dropdown list from api call data
function makeDropDownList(){
  fetchInfluencers.then(response => {
    response.json().then(data => {
      var dropdownlist = document.getElementById("dropdownlist");
      for (i = 0; i <= data.data.length; i++) {
        var option = document.createElement("option");
        option.setAttribute("label",data.data[i])
        option.setAttribute("value",data.data[i])
        dropdownlist.add(option);
      }
    })
  })
}

makeDropDownList()



window.onload = function() {



  //Listen to changes in dropdown menu and fetch follows by selected twitter user when selected
  document.getElementById("dropdownlist").addEventListener("change", function() {
    theCurrentFollowsUrlTemp = theCurrentFollowsUrl
    theCurrentFollowsUrlTemp = theCurrentFollowsUrl + this.value
    var fetchCurrentFollows = fetch(theCurrentFollowsUrlTemp)
    fetchCurrentFollows.then(response => {
      response.json().then(data => {
        while (document.getElementById("followsByInfluencerDiv").hasChildNodes()){
          document.getElementById("followsByInfluencerDiv").removeChild(document.getElementById("followsByInfluencerDiv").lastChild)
        }

        Object.entries(data.data).forEach((key) => {
          console.log(`${key[1]}`);
          var a = document.createElement('a')
          var link = document.createTextNode("@"+key[1]);
          a.appendChild(link)
          a.title = "@"+key[1]
          a.href = "http://www.twitter.com/"+key[1]
          var newLink = document.createElement("a")
          a.setAttribute("id", "follows")
          document.getElementById("followsByInfluencerDiv").appendChild(a)
          document.getElementById("followsByInfluencerDiv").appendChild(document.createElement("br"))
        })
      })
    })
  }
  );

}



function getTimestampString(timestamp) {
  timestamp = Number(timestamp)*1000
  var date = new Date(timestamp)
  
  return date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getFullYear()+" "+date.getHours()+":"+date.getMinutes()+" UTC +3"
}