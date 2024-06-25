python.pythonGenerator.forBlock['move'] = function(block) {  var dropdown_direction = block.getFieldValue('DIRECTION');
  var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);

  var directionFunction = dropdown_direction === 'FORWARD' ? 'forward' : 'backward';

  if (value_duration) {
    var code = `${directionFunction}(${value_speed}, ${value_duration})\n`;
  } else {
    var code = `${directionFunction}(${value_speed})\n`;
  }

  return code;
};

python.pythonGenerator.forBlock['turn'] = function(block) {  var dropdown_direction = block.getFieldValue('DIRECTION');
  var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);

  var directionFunction = dropdown_direction === 'LEFT' ? 'turn_left' : 'turn_right';

  if (value_duration) {
    var code = `${directionFunction}(${value_speed}, ${value_duration})\n`;
  } else {
    var code = `${directionFunction}(${value_speed})\n`;
  }
  return code;
};

python.pythonGenerator.forBlock['stop_rosa'] = function(block) {
  var code = `stop()\n`;
  return code;
};

python.pythonGenerator.forBlock['sleep'] = function(block) {
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
  var code = `sleep(${value_duration})\n`;
  return code;
};


python.pythonGenerator.forBlock['led'] = function(block) {
  var dropdown_led = block.getFieldValue('LED');
  var dropdown_color = block.getFieldValue('COLOR');
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
  var code;
  if (value_duration) {
    code = `active_led('${dropdown_led}', '${dropdown_color}', ${value_duration})\n`;
  } else {
    code = `active_led('${dropdown_led}', '${dropdown_color}')\n`;
  }
  return code;
};

python.pythonGenerator.forBlock['buzzer'] = function(block) {
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
  var code;
  if (value_duration) {
      code = `active_buzz(${value_duration})\n`;
  } else {
      code = `active_buzz()\n`;
  }
  return code;
};


python.pythonGenerator.forBlock['ground_sensor'] = function(block) {
  var sensor = Blockly.Python.valueToCode(block, 'DIRECTION', Blockly.Python.ORDER_ATOMIC);
  var code = `get_ground_value(${sensor})`
  return code;
};

