//const { inherits } = require("node:util")

//URLs for REST api calls
const theUrl = "http://localhost:5000/influencers"
var theCurrentFollowsUrl = "http://localhost:5000/follows?name="
var handleSearchUrl = "http://localhost:5000/handlesearch?handle="





window.onload = function() {
  
  //Listen for search button clicks
  document.getElementById("search").addEventListener("click", function() {
    console.log(window.screen.availHeight)
    console.log(window.screen.height)
    handleSearchUrlTemp = handleSearchUrl
    //Search field has to empty, no unnecessary api calls
    if (document.getElementById("handleToSearch").value == ""){
      document.getElementById("searchResults").textContent = "Can't be empty"
    }
    else{
      //If it is not empty then fetch data from api
      document.getElementById("searchResults").textContent = "Searching.."
      handleSearchUrlTemp = handleSearchUrl + document.getElementById("handleToSearch").value
      var fetchFollowsByHandle = fetch(handleSearchUrlTemp)
      fetchFollowsByHandle.then(response => {
        response.json().then(data => {
          //If result divs exist in html then delete them before printing new search results
          while (document.getElementById("results")){
            document.getElementById("results").outerHTML = ""
          }
          //Loop over entries and form message to be posted to page
          Object.entries(data.data).forEach(([key, value]) => {
            console.log(`${key}: ${value}`);
            var content = document.createTextNode("@"+key+" started following this handle at "+getTimestampString(value))
            var newDiv = document.createElement("div")
            newDiv.setAttribute("id", "results")
            newDiv.appendChild(content)
            document.getElementById("handleToSearchDiv").appendChild(newDiv)
            //document.body.insertBefore(newDiv, document.getElementById("searchResults"))
        document.getElementById("searchResults").textContent = ""
          });
        })
      })
    }
  })
  }



function getTimestampString(timestamp) {
  timestamp = Number(timestamp)*1000
  var date = new Date(timestamp)
  
  return date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getFullYear()+" "+date.getHours()+":"+date.getMinutes()+" UTC +3"
}