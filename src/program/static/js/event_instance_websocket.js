const webSocketBridge = new channels.WebSocketBridge();
var modals = {};

function toggleFavoriteButton(button) {
    if(button.getAttribute('data-state') == 'true') {
        favorite_button.classList.remove('btn-success');
        favorite_button.classList.add('btn-danger');
        favorite_button.innerHTML = '<i class="fa fa-minus"></i> Remove favorite';

        favorite_button.onclick = function(e) {
            button.setAttribute('data-state', 'false')
            webSocketBridge.send({action: 'unfavorite', event_instance_id: event_instance_id});
            toggleFavoriteButton(button)
        }
    } else {
        favorite_button.classList.remove('btn-danger');
        favorite_button.classList.add('btn-success');
        favorite_button.innerHTML = '<i class="fa fa-star"></i> Favorite';

        favorite_button.onclick = function(e) {
            button.setAttribute('data-state', 'true')
            webSocketBridge.send({action: 'favorite', event_instance_id: event_instance_id});
            toggleFavoriteButton(button)
        }

    }
}

webSocketBridge.connect('/schedule/');
webSocketBridge.socket.addEventListener('open', function() {
    webSocketBridge.send({action: 'init', camp_slug: '{{ camp.slug }}'});
});
webSocketBridge.listen(function(payload, stream) {
    if(payload['action'] == 'event_instance') {
        event_instance_id = payload['event_instance']['id'];
        modal = modals[event_instance_id];
        modal_title = modal.getElementsByClassName('modal-title')[0];
        modal_title.innerHTML = payload['event_instance']['title']
        modal_body_content = modal.getElementsByClassName('modal-body-content')[0];
        modal_body_content.innerHTML = payload['event_instance']['abstract'];
        more_button = modal.getElementsByClassName('more-button')[0];
        more_button.setAttribute('href', payload['event_instance']['url']);
        favorite_button = modal.getElementsByClassName('favorite-button')[0];
        if(payload['event_instance']['is_favorited'] !== undefined) {
            favorite_button.setAttribute('data-state', payload['event_instance']['is_favorited'])
            toggleFavoriteButton(favorite_button);
        } else {
            favorite_button.remove();
        }

        speakers_div = modal.getElementsByClassName('speakers')[0];
        speakers = payload['event_instance']['speakers'];
        for(speaker_id in speakers) {
            var speaker = speakers[speaker_id];
            var speaker_li = document.createElement('li');
            var speaker_a = document.createElement('a');
            speaker_a.setAttribute('href', speaker['url']);
            speaker_a.appendChild(document.createTextNode(speaker['name']));
            speaker_li.appendChild(speaker_a);
            speakers_div.appendChild(speaker_li);
        }
    }
});

function openModal(e) {
    e.preventDefault();

    // Avoid that clicking the text in the event will bring up an empty modal
    target = e.target;
    if (e.target !== this) {
        target = e.target.parentElement
    }

    event_instance_id = target.dataset['eventinstanceId'];

    modal = modals[event_instance_id];

    if(modal == undefined) {
        template = document.getElementById('event-template');
        modal = template.cloneNode(true);
        body = document.getElementsByTagName('body')[0];
        body.appendChild(modal);
        modal.setAttribute('id', 'event-modal-' + event_instance_id)
        modals[event_instance_id] = modal;
    }

    $('#event-modal-' + event_instance_id).modal();
    webSocketBridge.send({action: 'get_event_instance', event_instance_id: event_instance_id})
}


function init_modals(event_class_name) {
  var event_elements = document.getElementsByClassName(event_class_name);

  for (var event_id in event_elements) {
      event_element = event_elements.item(event_id);
      event_element.onclick = openModal
  }
}