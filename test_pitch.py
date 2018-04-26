from audio import produce_soundfile
from play import SOUND_BY_PITCHES
import wave

TEST_PITCH_DIR = './test_pitch/'
TEST_RATE = 720
TEST_REPEATS = 100

if __name__ == '__main__':
	for note, (sound, voice) in SOUND_BY_PITCHES.iteritems():
		produce_soundfile(sound*TEST_REPEATS, voice, TEST_RATE, TEST_PITCH_DIR+note+'.wav')
	def _get_repeats_per_second(note):
		w = wave.open(TEST_PITCH_DIR+note+'.wav', mode='rb')
		time = float(w.getnframes()) / w.getframerate()
		w.close()
		return float(TEST_REPEATS) / time
	repeats_per_second = {
		note: _get_repeats_per_second(note) for note in SOUND_BY_PITCHES.iterkeys()
	}
	with open('repeats_per_second.txt', 'w') as f:
		f.writelines([str(repeats_per_second)])