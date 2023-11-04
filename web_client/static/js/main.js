/*
This file contains the code that will run on the client side.
References:
- Chatbot: https://codepen.io/zenworm/pen/KqLNPm
*/

const $ChatInput = $('.ChatInput-input');

// Setup socket.io
var socket = io();

socket.on('connect', ()=> {
  socket.emit('my event', { data: 'I\'m connected!' });
});

socket.on('reply_to', (data) => {
  console.log(data);
  replyMsg(data);
});

$ChatInput.keyup(function (e) {
  if (e.shiftKey && e.which === 13) {
    e.preventDefault();
    return;
  }
  const msgTime = formatMsgTime();
  const $this = $(this);
//  console.log($this.html());
  if (e.which === 13) {
    const msg = $this.html();
    console.log(msg.split('<div>')[0]);
    sendMsg(msg.split('<div>')[0]);
    $this.html('');
    $('.ChatWindow').append(`
      <div class="ChatItem ChatItem--expert"> 
        <div class="ChatItem-meta">
          <div class="ChatItem-avatar">
            <img class="ChatItem-avatarImage" src="https://randomuser.me/api/portraits/women/0.jpg">
          </div>
        </div>
        <div class="ChatItem-chatContent">
          <div class="ChatItem-chatText">` + msg + `</div>
          <div class="ChatItem-timeStamp"><strong>Me</strong> · ${msgTime}</div>
        </div>
      </div>
    `);

    return $('.ChatWindow').animate({ scrollTop: $('.ChatWindow').prop('scrollHeight') }, 500);
  }
});

// Send and receive messages
function sendMsg(msg) {
  socket.emit('message', { data: msg });
}

//sendBtn.click(()=> {
//  sendMsg();
//});

function replyMsg(msg) {
  const msgTime = formatMsgTime();
  $('.ChatWindow').append(`
    <div class="ChatItem ChatItem--user">
      <div class="ChatItem-meta">
        <div class="ChatItem-avatar">
          <img class="ChatItem-avatarImage" src="https://randomuser.me/api/portraits/women/0.jpg">
        </div>
      </div>
      <div class="ChatItem-chatContent">
          <div class="ChatItem-chatText">${msg}</div>
          <div class="ChatItem-timeStamp"><strong>Chatbot</strong> · ${msgTime}</div>
        </div>
    </div>
  `);
  return $('.ChatWindow').animate({ scrollTop: $('.ChatWindow').prop('scrollHeight') }, 500);
}



// Date and time formatting
function formatMsgTime() {
  const now = new Date();
  const formatted = now.toLocaleString('en-US', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  });  // "Dec 19, 5:00"
  return formatted;
}

