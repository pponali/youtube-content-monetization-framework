"""
Extract and process transcripts from YouTube videos.
"""
import re
from typing import Dict, List, Any, Optional
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TranscriptExtractor:
    """Class to extract and process YouTube video transcripts."""
    
    def __init__(self):
        """Initialize the TranscriptExtractor."""
        # Initialize stopwords for keyword extraction
        self.stop_words = set(stopwords.words('english'))
    
    def get_transcript(self, video_id: str, languages: List[str] = ['en']) -> List[Dict[str, Any]]:
        """
        Get the transcript for a YouTube video.
        
        Args:
            video_id: YouTube video ID.
            languages: List of language codes to try, in order of preference.
            
        Returns:
            List of transcript segments, each containing 'text', 'start', and 'duration'.
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return transcript
        except TranscriptsDisabled:
            print(f"Transcripts are disabled for video ID: {video_id}")
            return []
        except NoTranscriptFound:
            print(f"No transcripts found for video ID: {video_id} in languages: {languages}")
            return []
        except Exception as e:
            print(f"Error retrieving transcript: {e}")
            return []
    
    def transcript_to_text(self, transcript: List[Dict[str, Any]]) -> str:
        """
        Convert transcript segments to a single text string.
        
        Args:
            transcript: List of transcript segments.
            
        Returns:
            Full transcript text.
        """
        return ' '.join(segment['text'] for segment in transcript)
    
    def extract_paragraphs(self, transcript_text: str) -> List[str]:
        """
        Split transcript text into meaningful paragraphs.
        
        Args:
            transcript_text: Full transcript text.
            
        Returns:
            List of paragraphs.
        """
        # Simple approach: split by sentences and group into paragraphs
        sentences = sent_tokenize(transcript_text)
        
        paragraphs = []
        current_paragraph = []
        
        for sentence in sentences:
            current_paragraph.append(sentence)
            
            # Start a new paragraph after 2-5 sentences or based on content
            if len(current_paragraph) >= 3 or sentence.endswith(('?', '!')):
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        
        # Add any remaining sentences as a paragraph
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        return paragraphs
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract important keywords from text.
        
        Args:
            text: Input text.
            top_n: Number of top keywords to return.
            
        Returns:
            List of keywords.
        """
        # Tokenize and filter words
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words 
                         if word.isalnum() and word not in self.stop_words]
        
        # Calculate word frequency
        fdist = FreqDist(filtered_words)
        
        # Get top N keywords
        return [word for word, _ in fdist.most_common(top_n)]
    
    def detect_code_snippets(self, transcript_text: str) -> List[str]:
        """
        Attempt to detect code snippets in transcript text.
        
        Args:
            transcript_text: Full transcript text.
            
        Returns:
            List of potential code snippets.
        """
        # Look for common coding patterns in the transcript
        code_indicators = [
            r'function\s+\w+\s*\([^)]*\)\s*\{',  # JavaScript/C-like function
            r'def\s+\w+\s*\([^)]*\):',  # Python function
            r'class\s+\w+(\s*\([^)]*\))?:',  # Python class
            r'class\s+\w+\s*\{',  # JavaScript/Java class
            r'import\s+[\w.]+',  # Import statements
            r'from\s+[\w.]+\s+import',  # Python import
            r'const\s+\w+\s*=',  # JavaScript variable
            r'let\s+\w+\s*=',  # JavaScript variable
            r'var\s+\w+\s*=',  # JavaScript variable
            r'\w+\s*:\s*\w+',  # TypeScript/Swift type annotation
            r'<[a-zA-Z][^>]*>.*</[a-zA-Z][^>]*>',  # HTML/XML tags
        ]
        
        code_snippets = []
        
        for pattern in code_indicators:
            matches = re.findall(pattern, transcript_text)
            code_snippets.extend(matches)
        
        return code_snippets
    
    def extract_timestamps_with_topics(self, transcript: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract timestamps with potential topic changes.
        
        Args:
            transcript: List of transcript segments.
            
        Returns:
            List of dictionaries with 'time' and 'topic'.
        """
        if not transcript:
            return []
        
        timestamps = []
        window_size = 5  # Number of segments to consider for topic detection
        
        for i in range(0, len(transcript), window_size):
            window = transcript[i:i+window_size]
            if not window:
                continue
                
            window_text = ' '.join(segment['text'] for segment in window)
            start_time = window[0]['start']
            
            # Extract potential topic from this window of text
            keywords = self.extract_keywords(window_text, top_n=3)
            topic = ' '.join(keywords)
            
            timestamps.append({
                'time': start_time,
                'topic': topic
            })
        
        return timestamps
    
    def process_transcript(self, video_id: str) -> Dict[str, Any]:
        """
        Process a video transcript to extract structured information.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Dictionary containing processed transcript information.
        """
        transcript = self.get_transcript(video_id)
        
        if not transcript:
            return {
                'video_id': video_id,
                'success': False,
                'message': 'No transcript available'
            }
        
        transcript_text = self.transcript_to_text(transcript)
        paragraphs = self.extract_paragraphs(transcript_text)
        keywords = self.extract_keywords(transcript_text, top_n=20)
        code_snippets = self.detect_code_snippets(transcript_text)
        timestamps = self.extract_timestamps_with_topics(transcript)
        
        return {
            'video_id': video_id,
            'success': True,
            'full_text': transcript_text,
            'paragraphs': paragraphs,
            'keywords': keywords,
            'code_snippets': code_snippets,
            'timestamps': timestamps
        }
