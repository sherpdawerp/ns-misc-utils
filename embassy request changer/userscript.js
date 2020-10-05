// ==UserScript==
// @name     embassy button adder
// @namespace https://github.com/abrow425/ns-misc-utils
// @version  1
// @author   SherpDaWerp
// @grant    none
// @include	 https://www.nationstates.net/page=region_admin*
// ==/UserScript==

function readURLParameters(pathname) {
 		var parameters = pathname.split("/");
    var paramlist = {};

    for (a = 1; a < parameters.length; a++) {
        var paramsplit = parameters[a].split("=");

        paramlist[paramsplit[0]] = paramsplit[1];
    }

  	return paramlist;
}

function switch_embassy_request() {
  var this_region = readURLParameters(window.location.pathname).region;
  var new_region = document.getElementById("embassy_switch_text").value;
  var new_region_url = new_region.replace(/ /g,"_");
  
  const emb_form = document.querySelector('html#page_region_admin body#loggedin div#main div#content div.divindent form');
  emb_form.action = '/page=region_control/region='.concat(new_region_url);
 
  var new_btn_text = 'Request embassies between '.concat(new_region, ' and ', this_region);
  
  const request_button = document.evaluate('/html/body/div[3]/div/div[3]/form/p/button', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
  request_button.textContent = new_btn_text;
  
}

(async function() {
	const embassy_indented_block = document.getElementById('embassies').nextElementSibling;  
	
  embassy_indented_block.insertAdjacentHTML('afterbegin', '<div><label>Switch Embassy Request Region To: </label><input type="text" id="embassy_switch_text"></input><br><button class="button primary" id="embassy_switch_btn">Switch Embassy Request Region</button></div><br>');
 	
  document.getElementById('embassy_switch_btn').addEventListener("click", switch_embassy_request, false);

})();
