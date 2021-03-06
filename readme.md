# Say Command Song Generator

This app sings songs using only the `say` command from Mac Terminal, leveraging the fact that `say`, run on a short, repeated syllable spoken very quickly, can approximate a pitch.  For example,
```
say wuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwu --voice=Luciana --rate=720
```
approximates the pitch A3.  By varying the syllable and voice, it is possible to get a wide range of pitches.

Given a melody, this app composes a combination of `say` commands that sings this melody.  For example, [this command sequence](http://github.com/bricehuang/say-sing/blob/master/sample_out/birthday.txt) sings Happy Birthday.

## Getting Started

This app should work out of the box, on a computer with Mac Terminal and Python 2.7 installed.

## Usage

The main usage is
```
python make_song.py [in_file] [out_file]
```
This writes to `out_file` a `say` command that sings the melody from `in_file`.  Default in and out files are `in.txt` and `out.txt`.
For example:
```
python make_song.py sample_in/birthday.txt sample_out/birthday.txt
eval $(cat sample_out/birthday.txt)
```
writes a `say` command sequence for Happy Birthday to `sample_out/birthday.txt` and executes these commands.

The first line in each input file is the tempo in BPM, and each subsequent line is a note and duration in beats.  Currently supported notes are F2-F4.  See `sample_in/` for examples of input formatting.

### Changing the Pitch Map

The map from pitch to `(syllable, voice)` is stored in `config/pitch_map.config`.  Candidate `(syllable, voice)` combinations for each pitch are stored in `pitches.out`, in the format
```
(pitch_diff, purity, (syllable, voice))
```
where `pitch_diff` is the difference from the true note in cents, and `purity` is a 0-1 score of how clean the pitch is.

After changing the pitch map, run
```
python regenerate_configs.py
```
to regenerate auto-generated configs before running `make_song.py`.

### Methodology for Generating Pitch Data

For each `(syllable, voice)` combination, I extract a waveform from the `say` soundfile and Fourier transform it, then extract the largest frequencies.  The data-analysis scripts are as follows:
* `generate_voice_data.py`: processes all `(syllable, voice)` combinations for a given voice, and prints `(syllable, voice, frequency, goodness)` results to `outfiles/[voice].out`.  Usage: `python generate_voice_data.py [voice]`.
* `consolidate_voice_data.py`: consolidates the outfiles from `generate_voice_data.py`.  Finds candidate `(syllable, voice)` combinations for each pitch and prints them to `pitches.out`.
* `data_script_master.py`: dispatches `generate_voice_data.py` for each voice, then dispatches `consolidate_voice_data.py`.
* `play_test_pitch.py`: util script that plays a `say` command with given syllable and voice.  Usage: `python audio.py [syllable] [voice]`.

## License

This project is licensed under the MIT License.

## Acknowledgments

Thanks to Next 4W and the MIT Undergrad Math Lounge for putting up with my obnoxious sound experimentation :)
