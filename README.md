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

This addon is intended for autoselection of audio/subtitles in series (not Movies as Kodi already remembers last selected)

Just select whatever audio/subtitle you want for your episode in a series (while it is playing) and this addon will
try to apply these same settings when playing other episodes from the same series.

## Background

I like to watch movies/series with the orignal audio and Dutch (preferred) or English subtitles.

However in Kodi you can not setup multiple languages for subtitles.
Audio is often tagged (what I consider) wrong in my sources so Kodi can also not help there.

There are other auto select addons that try to guess the correct audio/subtitle tracks based on
tags/tracknames/genre or more complex logic. I found that these addons required quite some effort
to get setup correctly with a lot of going back and forth between playing an episode
and back to the addon settings and then still there were cases where it dod not work as expected
which then required debugging again.

So I decided to make an addon that does not try to guess, but just re-apply settings that were
set by the user before on other episodes.

This means that you need to once set the audio/subtitle correctly for the first episode
you watch of a series (if Kodi selects the "wrong" ones).
This is easily done when cycle audio/subtitle buttons are on your remote.
The addon will try to apply that setting for following episodes.

The downside of this method is that it _does_ require consistent naming of audio/subtitle tracks,
but consistency between episodes seems to be quite common judging from my collection.
