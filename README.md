# Saasbops

Select
Audio
And
Subtitle
Based
On
Previous
Selection

## Description

NOTE: This addon is intended for autoselection of audio/subtitles in series (not Movies as Kodi already remembers last selected)

Other auto select addons try to guess the correct audio/subtitle tracks based on tags/tracknames or more complex logic.
I found that these addons required quite some effort to get setup correctly with a lot of going back and forth between playing an episode and back to the addon settings.

This addon takes out the guessing and instead it tries to select the same
audio/subtitle track as selected for previous episodes in the series.

This means that you need to once set the audio/subtitle correctly for the first episode
you watch of a series (if Kodi selects the "wrong" ones).
This is easily done when cycle audio/subtitle buttons are on your remote.
The addon will try to apply that setting for following episodes.

The downside of this method is that it _does_ require consistent naming of audio/subtitle tracks,
but that seems to be quite common judging from my collection.

## Background

I like to watch movies/series with the orignal audio and Dutch (preferred) or English subtitles.

It is hard to make an autoselection for this case as a lot of sources don't have a proper language
set for the video track so you can not select origninal audio based on that. Some releases are dubs and
even though they include the original audio the dubbed track is set as default.

Subtitles should be easier except that Kodi does not allow to select multiple preferred subtitle languages.

Hence the need for a different selection method.
