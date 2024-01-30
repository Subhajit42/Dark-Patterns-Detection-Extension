function highlightContent(textsObj) {
  const allTextNodes = textNodesUnder(document.body);

  for (const [key, value] of Object.entries(textsObj)) {
    for (const string of value) {
      var matchingElements = allTextNodes.filter(textNode => textNode.textContent.includes(string));
      for (let textNode of matchingElements) {
        const textOffset = textNode.textContent.indexOf(string);
    
        const range = new Range();
        range.setStart(textNode, textOffset);
        range.setEnd(textNode, textOffset + string.length);
        
        const wrapper = document.createElement('span');
        wrapper.classList.add('dp-checker');
        range.surroundContents(wrapper);
        wrapper.setAttribute("style", `border: solid ${colorScheme[key]} 2px`);
        wrapper.setAttribute("title", `${key}`);
      }
    }
  }
}

           
function textNodesUnder(el) {
    const children = []
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, (node) => node.parentNode.nodeName !== 'SCRIPT')
    while (walker.nextNode()) {
      children.push(walker.currentNode)
    }
    return children
}

let url_ = window.location.href;
const colorScheme = {
  "Forced Action": "red",
  "Misdirection" : "orange",
  "Obstruction" : "gray",
  "Scarcity" : "yellow",
  "Sneaking" : "purple",
  "Social Proof" : "blue",
  "Urgency" : "pink"
};

document.addEventListener("contextmenu", () => {
        const i = fetch("http://127.0.0.1:5000/",{
          method: "POST",
          body: JSON.stringify(
            {"URL": url_}
            ),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
          }).then(
            (response)=>response.text()
          ).then( 
            (text)=>{
              console.log(text)
              highlightContent(JSON.parse(text));             
            }
        )
})
