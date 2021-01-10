-- BSPlaylistManager

-- song
CREATE TABLE song
(songID VARCHAR(6) UNIQUE NOT NULL,
hash CHAR(40) UNIQUE NOT NULL,
mapper TEXT NOT NULL,
PRIMARY KEY (songID)
);

-- playlist
CREATE TABLE playlist
(playlistID TEXT UNIQUE NOT NULL,
fileName TEXT NOT NULL,
keyword TEXT UNIQUE NOT NULL,
playlistTitle TEXT NOT NULL,
playlistAuthor TEXT,
playlistDescription TEXT,
Image TEXT,
isDeleted BOOLEAN,
PRIMARY KEY (playlistID)
);

-- playlistDetail
CREATE TABLE playlistDetail
(detailID TEXT UNIQUE NOT NULL,
playlistID TEXT NOT NULL,
songID VARCHAR(6) NOT NULL,
PRIMARY KEY (detailID)
);
