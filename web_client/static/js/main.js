/*
This file contains the code that will run on the client side.
References:
- Chatbot: https://codepen.io/zenworm/pen/KqLNPm
- Avatars: https://www.flaticon.com/authors/freepik
*/

const $ChatInput = $('.ChatInput-input');

// Setup socket.io
var socket = io();

socket.on('connect', () => {
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
      <div class="ChatItem ChatItem--user">
        <div class="ChatItem-meta">
          <div class="ChatItem-avatar">
            <img class="ChatItem-avatarImage" src="${IMG_DIR}bear.png">

          </div>
        </div>
        <div class="ChatItem-chatContent">
          <div class="ChatItem-chatText">` + msg + `</div>
          <div class="ChatItem-timeStamp"><strong>Me</strong> · ${msgTime}</div>
        </div>
      </div>
    `);

    $('.ChatWindow').animate({ scrollTop: $('.ChatWindow').prop('scrollHeight') }, 500);

    setTimeout(() => {
      $('.ChatWindow').append(`
      <div class="ChatItem ChatItem--chatbot">
        <div class="ChatItem-meta">
          <div class="ChatItem-avatar">
            <img class="ChatItem-avatarImage" src="${IMG_DIR}buddy.png">
          </div>
        </div>
        <div class="ChatItem-chatContent">
          <div class="ChatItem-chatText">
            <span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>
            <span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>
            <span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>
          </div>
          <div class="ChatItem-timeStamp"><strong>Chatbot</strong> · ${msgTime}</div>
        </div>
      </div>
    `);
    }, 500);
    $('.ChatWindow').animate({ scrollTop: $('.ChatWindow').prop('scrollHeight') }, 500);
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
  // Replace the spinner with the reply message
  const $lastChatbotMsg = $('.ChatItem--chatbot').last();
  // console.log($lastChatbotMsg);
  // if not exist, append, else replace
  if ($lastChatbotMsg.length === 0) {
    $('.ChatWindow').append(`
    <div class="ChatItem ChatItem--chatbot">
      <div class="ChatItem-meta">
        <div class="ChatItem-avatar">
          <img class="ChatItem-avatarImage" src="${IMG_DIR}buddy.png">
        </div>
      </div>
      <div class="ChatItem-chatContent">
          <div class="ChatItem-chatText">${msg}</div>
          <div class="ChatItem-timeStamp"><strong>Chatbot</strong> · ${msgTime}</div>
        </div>
    </div>
  `);
  } else {
    $lastChatbotMsg.find('.ChatItem-chatText').html(msg);
    $lastChatbotMsg.find('.ChatItem-timeStamp').html(`<strong>Chatbot</strong> · ${msgTime}`);
  }
  $('.ChatWindow').animate({ scrollTop: $('.ChatWindow').prop('scrollHeight') }, 500);
}


//   return $('.ChatWindow').animate({ scrollTop: $('.ChatWindow').prop('scrollHeight') }, 500);
// }



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

