// Initialize global state object
const globalState = {
  currentDisplay: [],
  output: '',
  calculation: '',
  lastOutput: '',
  lastElement: '',
  isNegativeInitiated: false,
  isSquareRootInitiated: false,
  negativeNumber: '',
  squareRoot: '',
  counter: 1,
  lastCalculation: '',
  lastResult: '',
  isCalculated: false,
};

document.addEventListener('click', handleButtonClick);

function handleButtonClick(event) {
  const target = event.target;
  const targetValue = getButtonValue(target);

  const targetId = target.id;

  if (targetId === 'advanced') {
    toggleAdvancedInputs();
    return;
  }

  if (!targetValue) return;

  globalState.output = targetValue;

  debug('values');
  processInput();
}

function extractStackInfo(stack) {
  const stackLines = stack.split('\n');
  const relevantLine = stackLines[1].trim();

  const regex = /(.*):(\d+):(\d+)/;
  const match = relevantLine.match(regex);

  if (match) {
    const path = match[1];
    const lineInfo = `${match[2]}:${match[3]}`;
    return { path, lineInfo };
  } else {
    return { path: '', lineInfo: '' };
  }
}

const message_style = [
  'font-weight: bold',
  'display: block',
  'width: 100%',
  'box-sizing: border-box',
  'font-family: monospace',
].join(';');

function debug(option = '', message = '', stack = '') {
  if (option === 'values') {
    values();
  } else if (option === 'message') {
    if (stack) {
      const { path, lineInfo } = extractStackInfo(stack);
      console.log(
        `%c${message}\n| at : line ${lineInfo.split(':')[0]} col ${
          lineInfo.split(':')[1]
        } |`,
        message_style
      );
    }
  }
}

function getButtonValue(target) {
  if (target.tagName.toLowerCase() === 'i') {
    return target.parentElement.value;
  }
  return target.value;
}

function toggleAdvancedInputs() {
  document.getElementById('advanced-inputs').classList.toggle('hidden');
}

function processInput() {
  if (globalState.isCalculated) {
    resetState();
    globalState.isCalculated = false;
    debug('message', 'Reset state after calculation', new Error().stack);
  }

  globalState.currentDisplay = display.value.split('');
  globalState.lastElement =
    globalState.currentDisplay[globalState.currentDisplay.length - 1];

  if (globalState.output === 'clear') {
    resetState();
    debug('message', 'Cleared display', new Error().stack);
    return;
  }

  if (!globalState.output || !validateInput()) {
    debug(
      'message',
      `Input not valid or missing  -->  || ${globalState.output} ||`,
      new Error().stack
    );
    return;
  }

  handleAdvancedInputs();

  if (globalState.output == '=') {
    evaluateCalculation();
  } else {
    updateDisplay();
  }
}

function validateInput() {
  const invalidStartCharacters = ['+', '-', '÷', 'x', '.', ')', '='];
  if (
    globalState.currentDisplay.length === 0 &&
    invalidStartCharacters.includes(globalState.output)
  ) {
    debug('message', 'Invalid start character', new Error().stack);
    return false;
  }

  const invalidSequences = [
    // 1.1 with 1.2 , 2.1 with 2.1 , 2.2 with 2.2 , 2.3 with 2.3
    ['+', '-', '÷', 'x', '.', '(', '(-)'], //1.1 (0)
    ['+', '-', '÷', 'x', '.', ')', '='], //1.2 (1)
    [')'], //2.1 (2)
    ['(-)'], //2.2 (3)
    ['square-root'], //2.3 (4)
  ];

  if (
    (invalidSequences[0].includes(globalState.lastOutput) &&
      invalidSequences[1].includes(globalState.output)) ||
    (invalidSequences[2].includes(globalState.lastOutput) &&
      invalidSequences[2].includes(globalState.output)) ||
    (invalidSequences[3].includes(globalState.lastOutput) &&
      invalidSequences[3].includes(globalState.output)) ||
    (invalidSequences[4].includes(globalState.lastOutput) &&
      invalidSequences[4].includes(globalState.output))
  ) {
    debug('message', 'Invalid sequence detected', new Error().stack);
    return false;
  }

  if (!globalState.currentDisplay.includes('(') && globalState.output === ')') {
    debug('message', 'No opening bracket', new Error().stack);
    return false;
  }

  if (
    !(
      globalState.isNegativeInitiated === true ||
      globalState.isSquareRootInitiated === true
    ) &&
    globalState.currentDisplay.includes('(') &&
    !globalState.currentDisplay.includes(')') &&
    globalState.output === '='
  ) {
    debug(
      'message',
      'No closing bracket (ignoring negative number and square root)',
      new Error().stack
    );
    return false;
  }

  if (
    !(
      ['+', '-', '÷', 'x'].includes(globalState.lastOutput) ||
      globalState.currentDisplay.length === 0
    ) &&
    (globalState.output === '(' || globalState.output === 'square-root' || globalState.output === '(-)')
  ) {
    debug('message', 'Invalid position of (opening bracket || square root || negative number)', new Error().stack);
    return false;
  }

  if (
    globalState.calculation.split('')[0] === '(' &&
    globalState.calculation.split('')[1] === '-' &&
    !globalState.currentDisplay
      .slice(2)
      .some((char) => ['+', '-', 'x', '÷', '√'].includes(char)) &&
    globalState.output === '='
  ) {
    debug(
      'message',
      'Invalid equals sign usage(no operators - negative number)',
      new Error().stack
    );
    return false;
  }

  if (
    globalState.output === '=' &&
    !globalState.currentDisplay.some((char) =>
      ['+', '-', 'x', '÷', '√'].includes(char)
    )
  ) {
    debug(
      'message',
      'Invalid equals sign usage(no operators)',
      new Error().stack
    );
    return false;
  }

  return true;
}

function handleAdvancedInputs() {
  if (globalState.output === '(-)') {
    globalState.isNegativeInitiated = true;
  } else if (globalState.isNegativeInitiated) {
    globalState.negativeNumber = globalState.output;
  }

  if (globalState.output === 'square-root') {
    globalState.isSquareRootInitiated = true;
  } else if (globalState.isSquareRootInitiated) {
    globalState.squareRoot = globalState.output;
  }

  if (
    globalState.negativeNumber !== '' &&
    ['+', '-', 'x', '÷', '='].includes(globalState.output)
  ) {
    globalState.calculation += ')';
    resetState('negativeNumber');
    globalState.isNegativeInitiated = false;
  }

  if (
    globalState.squareRoot !== '' &&
    ['+', '-', 'x', '÷', '='].includes(globalState.output)
  ) {
    display.value += ')';
    globalState.calculation += ')';
    resetState('squareRoot');
    globalState.isSquareRootInitiated = false;
  }
}

function updateDisplay() {
  if (globalState.output === '(-)') {
    display.value += '-';
    globalState.lastOutput = '(-)';
    globalState.calculation += '(-';
    return;
  }

  if (globalState.output === 'square-root') {
    display.value += '√(';
    globalState.lastOutput = '√';
    globalState.calculation += 'Math.sqrt(';
    return;
  }

  display.value += ['+', '-', 'x', '÷'].includes(globalState.output)
    ? ` ${globalState.output} `
    : globalState.output;
  globalState.lastOutput = globalState.output;

  globalState.calculation += globalState.output
    .replace('x', '*')
    .replace('÷', '/');

  debug('values');
}

function values() {
  console.clear();
  console.group('Values');
  console.log(`Display: ${display.value}`);
  console.log(
    'Current display array length: ' + globalState.currentDisplay.length
  );
  for (const key in globalState) {
    if (globalState.hasOwnProperty(key)) {
      console.log(`${key}: ${globalState[key]}`);
    }
  }
  console.groupEnd();
}

function evaluateCalculation() {
  globalState.lastCalculation = display.value;
  resetState('display');

  try {
    let result = eval(globalState.calculation);
    if (result % 1 != 0) {
      result = result.toFixed(3).toString();
    } else {
      result = result.toString();
    }
    result = result.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    display.value = `= ${result}`;
    globalState.isCalculated = true;
    globalState.lastResult = display.value;
    debug('values');
    showResults();
  } catch (error) {
    display.value = 'Error in calculation';
    console.log(error);
  }
}

function resetState(option = 'all') {
  if (option === 'all') {
    display.value = '';
    globalState.calculation = '';
    globalState.negativeNumber = '';
    globalState.squareRoot = '';
  } else {
    globalState[option] = '';
  }
}

function showResults() {
  const listItem = document.createElement('li');
  listItem.id = 'list_item' + globalState.counter;
  document.getElementById('results').prepend(listItem);

  const calculationDisplay = document.createElement('p');
  calculationDisplay.id = 'display_calculation';
  calculationDisplay.textContent = globalState.lastCalculation;

  const resultDisplay = document.createElement('h5');
  resultDisplay.id = 'display_result';
  resultDisplay.textContent = globalState.lastResult;

  listItem.append(calculationDisplay, resultDisplay);
  globalState.counter++;
}
