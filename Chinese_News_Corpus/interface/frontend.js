function update_page(response) {
    var div = document.getElementById("show_article")
    div.innerHTML = response;

}

function submit_search(){
var form = document.getElementById("search_form")
    var formData = new FormData(form);
    var searchParams = new URLSearchParams(formData);
    var queryString = searchParams.toString();
    xmlHttpRqst = new XMLHttpRequest( )
    xmlHttpRqst.onload = function(e) {update_page(xmlHttpRqst.response);} 
    xmlHttpRqst.open( "GET", "/?" + queryString);
    xmlHttpRqst.send();
}

function annotation(obj){
    xmlHttpRqst = new XMLHttpRequest( )
    xmlHttpRqst.onload = function(e) {update_page(xmlHttpRqst.response);} 
    xmlHttpRqst.open( "GET", "/?polarity=" + obj.id);
    xmlHttpRqst.send();
}
