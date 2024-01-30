window.onload = function () {
  document.getElementById("submit").onclick = function () {
    chrome.tabs.create({
      url: "http://127.0.0.1:5000/feedback",
    });
  };

  document.getElementById("link").onclick = function () {
    chrome.tabs.create({
      url: "https://www.deceptive.design/",
    });
  };
};
