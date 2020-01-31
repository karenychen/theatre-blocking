/* actor.js - Theatre blocking JavaScript */
"use strict";
console.log("actor.js"); // log to the JavaScript console.

// Function to remove all blocking parts from current window
function removeAllBlocks() {
  blocks.innerHTML = "";
}

/* Function to add a blocking part to browser window */
function addScriptPart(scriptText, startChar, endChar, position) {
  const scriptPartText = scriptText.slice(startChar, endChar + 1);
  const part = blocks.children.length + 1;

  const html = `<h4>Part ${part}</h4>
          <p><em>"${scriptPartText}"</em></p>
          <p>Stage Position: <strong>${position}</strong></p>`;

  const block = document.createElement("div");
  block.className = "col-lg-12";
  block.innerHTML = html;
  blocks.appendChild(block);
}

function visualize() {
  let scriptBlocks = getBlockingDetailsOnScreen();

  // check if there are valid script blocking info on screen before visualization
  if (scriptBlocks.length === 0) {
    alert("Please get valid script blocking information before visualization.");
    return;
  }
  startVisualize(scriptBlocks);
  setTimeout(() => {
    clearPosition();
  }, 2000 * scriptBlocks.length);
}

function startVisualize(scriptBlocks) {
  clearPosition();
  for (let i = 0; i < scriptBlocks.length; i++) {
    (function() {
      let k = i;
      let blocks = scriptBlocks[k];
      setTimeout(() => {
        clearPosition();
        showScriptLine(blocks.text);
        let position = blocks.position;
        let part = blocks.part;
        showPosition(part, position);
      }, 2000 * k);
    })();
  }
}

function showScriptLine(line) {
  document.querySelector("#script-line").innerHTML = line;
  console.log(line);
}

// show position of actors on the blocking visualization grids
function showPosition(part, position) {
  document.querySelector("#position" + position).innerHTML = "Part " + part;
  console.log("#position" + position);
}

function clearPosition() {
  for (let i = 1; i <= 8; i++) {
    document.querySelector("#position" + i).innerHTML = "";
  }
  document.querySelector("#script-line").innerHTML = "";
}

// Function to add the example block (when clicking the example block button)
function getExampleBlock() {
  const url = "/example";

  // A 'fetch' AJAX call to the server.
  fetch(url)
    .then(res => {
      //// Do not write any code here
      return res.json();
      //// Do not write any code here
    })
    .then(jsonResult => {
      // This is where the JSON result (jsonResult) from the server can be accessed and used.
      console.log("Result:", jsonResult);
      // Use the JSON to add a script part
      addScriptPart(jsonResult[0], jsonResult[1], jsonResult[2], jsonResult[3]);
    })
    .catch(error => {
      // if an error occured it will be logged to the JavaScript console here.
      console.log("An error occured with fetch:", error);
    });
}

/* This function returns a JavaScript array with the information about blocking displayed
in the browser window.*/
function getBlockingDetailsOnScreen() {
  // this array will hold
  const allBlocks = [];

  // go through all of the script parts and scrape the blocking informatio on the screen
  for (let i = 0; i < blocks.children.length; i++) {
    const block = {};
    const blockElement = blocks.children[i];
    block.part = i + 1;
    block.text = blockElement.children[1].textContent;
    block.position = blockElement.children[2].children[0].innerHTML;
    allBlocks.push(block);
  }

  // Look in the JavaScript console to see the result of calling this function
  return allBlocks;
}

// add feedback for 404 recources not found
function showNotFound() {
  document.querySelector("#feedback").innerHTML = "The script is not found.";
  document.querySelector("#feedback").setAttribute("style", "color: red");
}

// a helper function for checking validity of input
function isNumeric(value) {
  return /^-{0,1}\d+$/.test(value);
}

/* Write the code to get the blocking for a particular script and actor */
function getBlocking() {
  // Remove any existing blocks
  removeAllBlocks();

  // Get the script and actor numbers from the text box.
  const scriptNumber = scriptNumText.value;
  const actorNumber = actorText.value;

  if (!isNumeric(scriptNumber) || !isNumeric(actorNumber)) {
    alert("Please enter a valid number.");
    return;
  }

  console.log(
    `Get blocking for script number ${scriptNumber} for actor ${actorNumber}`
  );

  const url = "/script/" + scriptNumber;

  // A 'fetch' AJAX call to the server.
  fetch(url)
    .then(res => {
      if (res.status == 404) {
        showNotFound();
      }
      return res.json();
    })
    .then(jsonResult => {
      // This is where the JSON result (jsonResult) from the server can be accessed and used.
      console.log("Result:", jsonResult);
      // Use the JSON to add a script part

      const script = jsonResult[0];
      console.log(script);
      const blocks = jsonResult[1];
      const actorIdMap = jsonResult[2];
      const actorName = actorIdMap[actorNumber];
      let actorPosition = "";

      for (let i = 0; i < blocks.length; i++) {
        let actors = blocks[i].actors;
        let positions = blocks[i].positions;
        for (let j = 0; j < actors.length; j++) {
          if (actors[j] === actorName) {
            actorPosition = positions[j];
          }
        }

        addScriptPart(script, blocks[i].start, blocks[i].end, actorPosition);
      }
    })
    .catch(error => {
      // if an error occured it will be logged to the JavaScript console here.
      console.log("An error occured with fetch:", error);
    });
}
