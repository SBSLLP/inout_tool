let workTime = 0; // Time in seconds
let timerInterval;
let isCheckedIn = false; // Track check-in status

// Fetch logged-in user and update the UI
document.addEventListener('DOMContentLoaded', function() {
  fetch('/api/user/')
    .then(response => response.json())
    .then(data => {
      document.getElementById('username').textContent = data.username;
    });

  // Check if user is already checked in
  checkUserStatus();
});

// Check user status (if already checked in)
function checkUserStatus() {
  fetch('/api/attendance/')
    .then(response => response.json())
    .then(data => {
      if (data.length > 0 && data[0].check_out_time === null) {
        isCheckedIn = true;
        document.getElementById('btnIn').disabled = true;
        document.getElementById('btnOut').disabled = false;
        startTimer();
      } else {
        isCheckedIn = false;
        document.getElementById('btnIn').disabled = false;
        document.getElementById('btnOut').disabled = true;
      }
    });
}

// Start timer when the user checks in
function startTimer() {
  timerInterval = setInterval(() => {
    workTime++;
    document.getElementById('workTimer').textContent = formatTime(workTime);
  }, 1000);
}

// Stop the timer
function stopTimer() {
  clearInterval(timerInterval);
}

// Handle check-in
document.getElementById('btnIn').addEventListener('click', function() {
  fetch('/api/attendance/check-in/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')  // CSRF Token
    }
  })
  .then(response => {
    if (response.ok) {
      isCheckedIn = true;
      document.getElementById('btnIn').disabled = true;
      document.getElementById('btnOut').disabled = false;
      startTimer();
    } else {
      alert('Error: Already checked in.');
    }
  });
});

// Handle check-out
document.getElementById('btnOut').addEventListener('click', function() {
  fetch('/api/attendance/check-out/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')  // CSRF Token
    }
  })
  .then(response => {
    if (response.ok) {
      isCheckedIn = false;
      document.getElementById('btnIn').disabled = false;
      document.getElementById('btnOut').disabled = true;
      stopTimer();
    } else {
      alert('Error: No active check-in.');
    }
  });
});

// Utility function to get the CSRF token (for Django POST requests)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
