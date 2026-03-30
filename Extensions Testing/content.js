// Listen for messages from the popup
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.action === "getHint") {
      // Send a request to the Flask server to get a hint
      chrome.runtime.getURL('/get_hint')
        .then(response => response.json())
        .then(data => {
          // Modify the DOM to display the hint
          console.log('Hint:', data.hint);
        });
    } else if (request.action === "solvePuzzle") {
      // Send a request to the Flask server to solve the puzzle
      chrome.runtime.getURL('/solve_puzzle')
        .then(response => response.json())
        .then(data => {
          // Modify the DOM to display the solution
          console.log('Solution:', data.solution);
        });
    }
  }
);
