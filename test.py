video_msg = { 'type': 'video', 'author': 'support', 'data': { 'text': '...or not?', 'video': {'title': 'Honda 2019', 'text': 'Hello', 'source': 'youtube', 'url': 'https://www.youtube.com/embed/Wi8skWmobkY'} } }
system_msg = { 'type': 'system', 'data': { 'text': 'User changed security key', 'meta': '04-08-2018 15:57' } }
list_msg = { 'type': 'list',
      'author': 'support',
      'data': { 'text': 'No forget the story. ',
        'top_element_style': 'large',
        'elements': [{
          'title': 'Test Card 1',
          'subtitle': 'This is a test message',
          'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
          'buttons': [
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"},
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"}] },
        {
          'title': 'Test Card 2',
          'subtitle': 'This is a test message',
          'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
          'buttons': [
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"},
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"}]
        },
        {
          'title': 'Test Card 3',
          'subtitle': 'This is a test message',
          'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
          'buttons': [
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"},
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"}]
        },
        {
          'title': 'Test Card 4',
          'subtitle': 'This is a test message',
          'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
          'buttons': [
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"},
            {'title': "You've got to have a story.",
              'payload': "You've got to have a story"}]
        }
        ] } }

image_msg = { 'type': 'image',
      'author': 'support',
      'data': { 'text': 'No forget the story. ',
    'elements':
    [
      { 'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg' },
      { 'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
        'title': 'Image 1',
        'text': 'text' },
      { 'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
        'title': 'Image 1',
        'text': 'text' }
    ]
      } }

card_msg = { 'type': 'card',
      'author': 'support',
      'data': { 'text': 'No forget the story. ',
        'elements': [
          { 'name': 'file.mp3',
            'title': 'Test Card 1',
            'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
            'buttons': [
              {'title': "You've got to have a story.",
                'payload': "You've got to have a story"},
              {'title': "You've got to have a story.",
                'payload': "You've got to have a story"}]
          },
          { 'name': 'file.mp3',
            'title': 'Test Card 2',
            'url': 'https://blissmotorsimages.s3.us-east-2.amazonaws.com/dthonda/images/thumbs/big/000ce3ac068721f7857fcf7aeb949d7975c4a060.jpg',
            'buttons': [
              {'title': "You've got to have a story.",
                'payload': "You've got to have a story"},
              {'title': "You've got to have a story.",
                'payload': "You've got to have a story"}]
          }
        ] } }
button_msg = { 'type': 'button',
      'author': 'support',
      'data': { 'text': 'What about suggestions?',
    'buttons':
    [
      {'title': 'I am a button 1',
        'payload': 'I am testing 2'},
      {'title': 'I am a button 2',
        'payload': 'I am testing 2'},
      {'title': 'I am a button 3',
        'payload': 'I am testing 3'},
      {'title': 'I am a button 4',
        'payload': 'I am testing 4'},
      {'title': 'I am a button 5',
        'payload': 'I am testing 5'},
      {'title': 'I am a button 6',
        'payload': 'I am testing 6'},
      {'title': 'I am a button 7',
        'payload': 'I am testing 7'},
      {'title': 'I am a button 8',
        'payload': 'I am testing 8'},
      {'title': 'I am a button 9',
        'payload': 'I am testing 9'},
      {'title': 'I am a button 10',
        'payload': 'I am testing 10'},
      {'title': 'I am a button 11',
        'payload': 'I am testing 11'},
      {'title': 'I am a button 12',
        'payload': 'I am testing 12'},
      {'title': 'I am a button 1222222222222222222222222222222',
        'payload': 'I am testing 12'}
    ]
      }}
qr_msg = { 'type': 'text', 'author': 'support', 'data': { 'text': 'What about suggestions?' }, 'suggestions': ['Looks good!', "It's OK.", 'Uhh.. Do I really have to say something?', "This suggestion is way too long for css purpose. Let's make it long... Longer, and more and more.. Never ending."] }

messages = {
    'qr_msg': qr_msg,
    'image_msg': image_msg,
    'card_msg': card_msg,
    'list_msg': list_msg,
    'button_msg': button_msg,
    'system_msg': system_msg,
    'video_msg': video_msg
}
