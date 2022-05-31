const destName = JSON.parse(document.getElementById("dest-name").textContent);
const destId = JSON.parse(document.getElementById("dest-id").textContent);
const messageInputDom = document.getElementById("input");
const messagesDOM = document.getElementById("messagesBox");

const chatSocket = new WebSocket(
  `ws://${window.location.host}/ws/chat/@me/${destId}/`
);

function sendFunc(ev) {
  const message = messageInputDom.value;
  if (message === "") {
    return;
  }
  chatSocket.send(
    JSON.stringify({
      message: message,
    })
  );
  messageInputDom.value = "";
  // Scroll down TODO
  messagesDOM.scrollTop = messagesDOM.scrollHeight;
}

messageInputDom.addEventListener("keypress", (ev) => {
  if (ev.key === "Enter") {
    ev.preventDefault();
    sendFunc(ev);
  }
});

document.querySelector("#send").onclick = sendFunc;

chatSocket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  let msg;
  const dateOptions = {
    // dateStyle: "full",
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    hour12: false,
  };
  const newTimestamp = new Date(data.timestamp).toLocaleString(
    "en",
    // dateOptions
  );
  if (data.username != destName) {
    msg = `<div class="chat-message-right mb-4">
                    <div>
                        <img src="https://bootdey.com/img/Content/avatar/avatar1.png"
                            class="rounded-circle mr-1" alt="" width="40" height="40">
                    </div>
                    <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                        <div class="font-weight-bold mb-1">You</div>
                        ${data.text}
                    </div>
                    <div class="text-muted small text-nowrap mt-2">${newTimestamp}</div>
                </div>`;
  } else {
    msg = `<div class="chat-message-left mb-4">
                    <div>
                        <img src="https://bootdey.com/img/Content/avatar/avatar2.png"
                            class="rounded-circle mr-1" alt="" width="40" height="40">
                    </div>
                    <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                        <div class="font-weight-bold mb-1">${data.username}</div>
                        ${data.text}
                    </div>
                    <div class="text-muted small text-nowrap mt-2">${newTimestamp}</div>
                </div>`;
  }
  messagesDOM.innerHTML += msg;

  //   document.querySelector("#chat-text").value += data.username + " > " + data.message + "\n";
};
