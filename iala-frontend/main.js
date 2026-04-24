// Generate a random user ID for the session
const userId = 'user_' + Math.random().toString(36).substring(2, 9);
let sessionId = null;
let currentConcept = 'Basic Finance'; // Default target topic

// DOM Elements
const chatHistory = document.getElementById('chat-history');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const conceptBadge = document.getElementById('current-concept');
const masteryValue = document.getElementById('mastery-value');
const masteryFill = document.getElementById('mastery-fill');
const engagementValue = document.getElementById('engagement-value');
const engagementFill = document.getElementById('engagement-fill');

// Initialization
async function initSession() {
  addMessage('System', 'Initializing connection to Socratic Engine...', 'agent');
  try {
    const response = await fetch('/api/session/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, target_topic: currentConcept })
    });
    
    if (!response.ok) throw new Error('Failed to start session');
    
    const data = await response.json();
    sessionId = data.session_id;
    currentConcept = data.concept;
    conceptBadge.textContent = currentConcept;
    
    // Clear history and add initial message
    chatHistory.innerHTML = '';
    addMessage('IALA Agent', data.message, 'agent', 'Instruction');
    
    // Enable inputs
    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.focus();
  } catch (error) {
    console.error('Init error:', error);
    addMessage('System Error', 'Could not connect to backend. Make sure the FastAPI server is running.', 'agent');
  }
}

// Handle Form Submission
chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = userInput.value.trim();
  if (!text || !sessionId) return;

  // Optimistic UI update
  addMessage('You', text, 'user');
  userInput.value = '';
  userInput.disabled = true;
  sendBtn.disabled = true;

  const loadingId = addLoadingIndicator();

  try {
    const response = await fetch('/api/session/respond', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        session_id: sessionId,
        concept: currentConcept,
        user_input: text
      })
    });

    if (!response.ok) throw new Error('Failed to send response');

    const data = await response.json();
    removeLoadingIndicator(loadingId);
    
    // Add agent response
    const aiResp = data.agent_response;
    addMessage('IALA Agent', aiResp.message, 'agent', aiResp.state);
    
    // Update Profile Stats
    updateProfile(data.student_profile);

  } catch (error) {
    console.error('Response error:', error);
    removeLoadingIndicator(loadingId);
    addMessage('System Error', 'Failed to communicate with Socratic Engine.', 'agent');
  } finally {
    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.focus();
  }
});

// UI Helpers
function addMessage(sender, text, type, meta = null) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${type}`;
  
  let contentHtml = `<div>${text}</div>`;
  if (meta && type === 'agent') {
    contentHtml += `<div class="message-meta">STATE: ${meta}</div>`;
  }
  
  msgDiv.innerHTML = contentHtml;
  chatHistory.appendChild(msgDiv);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addLoadingIndicator() {
  const id = 'loading-' + Date.now();
  const div = document.createElement('div');
  div.id = id;
  div.className = 'loading-dots';
  div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  chatHistory.appendChild(div);
  chatHistory.scrollTop = chatHistory.scrollHeight;
  return id;
}

function removeLoadingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function updateProfile(profile) {
  // Update Mastery
  const mPercent = Math.round(profile.mastery_level * 100);
  masteryValue.textContent = `${mPercent}%`;
  masteryFill.style.width = `${mPercent}%`;
  
  // Update Engagement
  const ePercent = Math.round(profile.engagement_score * 100);
  engagementValue.textContent = `${ePercent}%`;
  engagementFill.style.width = `${ePercent}%`;
}

// Start
document.addEventListener('DOMContentLoaded', initSession);
