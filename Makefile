clean:
	rm -f *.mp4 *.m4a *.webm *.mkv *.part

run: clean
	./youtube_downloader.py
