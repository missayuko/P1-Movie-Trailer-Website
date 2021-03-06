import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>JJ's Freshest Tomatoes!</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <link href='http://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
		/***************************************************************************
		Additional CSS3 to show plot on hover adapted from 
		https://css-tricks.com/slide-in-image-captions/ 
		and 
		http://geekgirllife.com/animate-text-over-images-on-hover-without-javascript/
		*****************************************************************************/
		
        figure {
            display: block;
            position: relative;
            overflow: hidden;
            margin: 0 20px 20px 0;
        }
        figcaption {
            position: absolute;
            background: rgba(0, 0, 0, 0.75);
            color: white;
            padding: 10px 20px;
            opacity: 0;
            -webkit-transition: all 0.6s ease;
            -moz-transition: all 0.6s ease;
            -o-transition: all 0.6s ease;
        }
        figure:hover figcaption {
            opacity: 1;
        }
        figure:before {
            content: "?";
            position: absolute;
            font-weight: 800;
            background: rgba(255, 255, 255, 0.75);
            text-shadow: 0 0 5px white;
            color: black;
            width: 24px;
            height: 24px;
            -webkit-border-radius: 12px;
            -moz-border-radius: 12px;
            border-radius: 12px;
            text-align: center;
            font-size: 14px;
            line-height: 24px;
            -moz-transition: all 0.6s ease;
            opacity: 0.75;
        }
        figure:hover:before {
            opacity: 0;
        }
        .image-grid img {
            -webkit-transition: all 300ms;
            -moz-transition: all 300ms;
            transition: all 300ms;
            max-width: 100%;
        }
        .image-grid img:hover {
            -webkit-transform: scale(1.4);
            -moz-transform: scale(1.4);
            transform: scale(1.4);
        }
        .image-grid:before {
            bottom: 10px;
            left: 10px;
        }
        .image-grid figcaption {
            left: 0;
            bottom: -30%;
        }
        .image-grid:hover figcaption {
            bottom: 0;
        }
        body {
            font-family: "Roboto", sans-serif;
            padding-top: 80px;
        }
        h2,
        .h2 {
            font-family: "Raleway", sans-serif;
            font-size: 20px;
        }
        p {
            font-family: "Roboto", sans-serif;
            margin: 20 0 10px;
        }
        img {
            padding: 20px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            background-color: #eee;
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #ffb2b2;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .navbar-default {
            background-image: none;
            box-shadow: none;
            -webkit-box-shadow: none;
        }
        .navbar-header {
            float: left;
            padding: 15px;
            text-align: center;
            width: 100%;
        }
        .navbar-brand {
            float: none;
        }
        .navbar-default .navbar-brand {
            color: #f00;
        }
    </style>
    <script type="text/javascript" charset="utf-8">	// Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">JJ's Freshest Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
		
		{movie_tiles}
	  
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <h2>{movie_title}</h2>
    <figure class="image-grid">
        <img src="{poster_image_url}" width="220" height="342">
        <figcaption><strong>Plot: </strong>{plot}<br><strong>Cast:</strong>{cast}</figcaption>
    </figure>
    <br style="clear: both;">
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
			plot=movie.plot,
			cast=movie.cast
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible
