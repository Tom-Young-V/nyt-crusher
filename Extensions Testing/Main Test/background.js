// background.js
console.log("Extension loaded!");

chrome.commands.onCommand.addListener((command) => {
	console.log("command pressed A");
	if (command === "solvePuzzle") {
		console.log("command pressed B");
		// Find the active tab
		chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
			console.log("sending message");
			const activeTab = tabs[0];
			if (activeTab && activeTab.url.includes("https://wafflegame.net/daily")) {
				// Send a message to content.js
				chrome.tabs.sendMessage(activeTab.id, { action: "getEntireHTML" });
			}
		});
	}
});

// Detect navigation to the specified URL
chrome.webNavigation.onCompleted.addListener((details) => {
	if (details.url.includes("https://wafflegame.net/daily")) {
		console.log("Navigated to https://wafflegame.net/daily");
		// You can perform additional actions here.
	}
});
