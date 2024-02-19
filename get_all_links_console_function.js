function unique(a) {
  var seen = {};
  return a.filter(function(item) {
      return seen.hasOwnProperty(item) ? false : (seen[item] = true);
  });
}

function scrapeLinks(startsWith="", prefix="") {
  // Get all anchor elements on the webpage
  const anchors = document.getElementsByTagName('a');
  
  const links = [];

  // Loop through each anchor element
  for (let i = 0; i < anchors.length; i++) {
      const href = anchors[i].getAttribute('href');

      // Check if the href attribute starts with 'mailto:'
      if (href && href.startsWith(startsWith)) {
          links.push(prefix + href);
      }
  }

  return unique(links);
}