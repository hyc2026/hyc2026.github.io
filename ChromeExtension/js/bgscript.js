chrome.browserAction.onClicked.addListener(function (tab) {
  var url = tab.url;
  var hashStart = (url.indexOf('#') === -1) ? url.length : url.indexOf('#');
  var newUrl = url.substring(0, hashStart) + "#view=FitH,top"

  chrome.tabs.update(tab.id, {url: newUrl});
});