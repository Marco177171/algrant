// scroll to bottom on load
main = document.getElementById('main');
main.scrollTop = main.scrollHeight;
// web socket management
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${conversation_id}/`);
socket.onclose = function(event) {
	console.error('WebSocket closed unexpectedly:', event);
};

// new message
function sendMessage(event) {
	// Prevent the link's default navigation behavior
	event.preventDefault();
	const messageInput = document.getElementById('message_input');
	const messageText = messageInput.value;
	// create message in db
	fetch(`/new_message/${conversation_id}`, {
		method: 'POST',
		headers: {
			'X-CSRFToken': `${csrf_token}`,
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ 'message_text': messageText })
	})
	.then(messageInput.value = null)
	.then(response => response.json())
	.catch(error => console.error('Error:', error));
}

// compose and display message on the ui
socket.onmessage = function(event) {
	const data = JSON.parse(event.data);
	const messageList = document.getElementById('message-list'); // get container

	const newMessageDiv = document.createElement('div')

	const dividerElement = document.createElement('div');
	dividerElement.className = 'divider';

	const newMessageSender = document.createElement('a');
	newMessageSender.href = `/user_profile/${data.user}`;
	newMessageSender.textContent = `${data.user}`;

	const newMessageTimestamp = document.createElement('span');
	newMessageTimestamp.textContent = 'just now';

	const newMessageContent = document.createElement('p');
	newMessageContent.textContent = `${data.message}`;
	
	const messageMovesSpanText = document.createElement('span');
	messageMovesSpanText.textContent = 'message moves:';
	
	const deleteMessageAnchor = document.createElement('a');
	deleteMessageAnchor.onclick = "document.getElementById('delete-message-form-{{ message.id }}').submit()";
	deleteMessageAnchor.textContent = 'Delete';
	
	newMessageDiv.appendChild(dividerElement);
	newMessageDiv.appendChild(newMessageSender);
	newMessageDiv.appendChild(newMessageTimestamp);
	newMessageDiv.appendChild(newMessageContent);
	messageList.appendChild(newMessageDiv);
	
	if (data.user == `${request_user}`) {
		console.log('sent by me');
		newMessageDiv.style = "text-align:right"
		newMessageDiv.appendChild(messageMovesSpanText);
		newMessageDiv.appendChild(deleteMessageAnchor);
	}

	main.scrollTop = main.scrollHeight; // if you wish
};
