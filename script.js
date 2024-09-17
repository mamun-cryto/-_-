let playerHealth = 100;
let enemyHealth = 100;

// Function to update health status
function updateHealth() {
  document.getElementById("player-health").textContent = playerHealth;
  document.getElementById("enemy-health").textContent = enemyHealth;
}

// Function to display log messages
function logMessage(message) {
  const log = document.getElementById("log");
  const p = document.createElement("p");
  p.textContent = message;
  log.appendChild(p);
  log.scrollTop = log.scrollHeight;
}

// Attack function
function attack() {
  let playerDamage = Math.floor(Math.random() * 20) + 1;
  let enemyDamage = Math.floor(Math.random() * 15) + 1;

  enemyHealth -= playerDamage;
  playerHealth -= enemyDamage;

  logMessage(`You attacked the enemy and dealt ${playerDamage} damage!`);
  logMessage(`Enemy attacked you and dealt ${enemyDamage} damage!`);

  if (enemyHealth <= 0) {
    enemyHealth = 0;
    logMessage("You defeated the enemy!");
    disableActions();
  }

  if (playerHealth <= 0) {
    playerHealth = 0;
    logMessage("You were defeated by the enemy!");
    disableActions();
  }

  updateHealth();
}

// Defend function (reduces damage)
function defend() {
  let playerBlock = Math.floor(Math.random() * 10) + 1;
  let enemyDamage = Math.floor(Math.random() * 15) + 1 - playerBlock;

  if (enemyDamage < 0) enemyDamage = 0;

  playerHealth -= enemyDamage;

  logMessage(`You blocked and reduced the damage by ${playerBlock}!`);
  logMessage(`Enemy attacked and dealt ${enemyDamage} damage!`);

  if (playerHealth <= 0) {
    playerHealth = 0;
    logMessage("You were defeated by the enemy!");
    disableActions();
  }

  updateHealth();
}

// Heal function (restore health)
function heal() {
  let healing = Math.floor(Math.random() * 20) + 10;

  playerHealth += healing;
  if (playerHealth > 100) playerHealth = 100;

  logMessage(`You healed yourself and restored ${healing} health!`);

  updateHealth();
}

// Disable buttons after game ends
function disableActions() {
  document.querySelectorAll('.actions button').forEach(button => {
    button.disabled = true;
  });
}

// Restart the game
function restart() {
  playerHealth = 100;
  enemyHealth = 100;
  updateHealth();
  document.getElementById("log").textContent = '';
  document.querySelectorAll('.actions button').forEach(button => {
    button.disabled = false;
  });
  logMessage("Game restarted!");
}

// Initialize the health display on load
updateHealth();