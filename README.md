# CV Matchy-Matchy 🎯

A modern web application that analyzes your CV against job descriptions to provide personalized insights and customization suggestions.

## ✨ Features

- **📄 PDF Upload**: Upload your CV in PDF format
- **📝 Job Description Analysis**: Paste any job description for comparison
- **🎯 Match Percentage**: Get a clear percentage of how well you match
- **💪 Strengths Identification**: Discover what makes you stand out
- **🔧 Areas for Improvement**: Identify gaps and weaknesses
- **💡 Customization Suggestions**: Get actionable advice to improve your CV
- **🎨 Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- **🤖 AI-Powered Analysis**: Uses Hugging Face's free LLM for intelligent analysis

## 🏗️ Architecture

- **Frontend**: React with TypeScript and Tailwind CSS
- **Backend**: Python Flask API
- **LLM**: Hugging Face Inference API (free tier)
- **PDF Processing**: PyPDF2 for text extraction
- **Styling**: Modern, responsive design with Tailwind CSS

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js 14+
- Free Hugging Face API key

### 1. Clone and Setup

```bash
# Run the automated setup script
./setup.sh
```

### 2. Get API Key

1. Visit [Hugging Face](https://huggingface.co/settings/tokens)
2. Create a free account
3. Generate a new API token
4. Copy the token

### 3. Configure Environment

```bash
# Copy the example environment file
cp backend/env.example backend/.env

# Edit the .env file and add your API key
nano backend/.env
```

Add your API key:
```
HUGGINGFACE_API_KEY=your_api_key_here
```

### 4. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 5. Open the Application

Visit [http://localhost:3000](http://localhost:3000) in your browser.

## 🧪 Testing

Run the test script to verify everything is working:

```bash
python3 test_backend.py
```

## 📖 How to Use

1. **Upload Your CV**: Click the upload area and select your PDF CV
2. **Paste Job Description**: Copy and paste the job description you want to analyze against
3. **Analyze**: Click the "Analyze CV" button
4. **Review Results**: 
   - Check your match percentage
   - Review your strengths
   - Identify areas for improvement
   - Follow the customization suggestions

## 🔧 Technical Details

### Backend API Endpoints

- `GET /api/health` - Health check
- `POST /api/analyze` - CV analysis endpoint

### Analysis Process

1. **PDF Text Extraction**: Converts your PDF to text
2. **Content Analysis**: Compares CV content with job requirements
3. **LLM Processing**: Uses AI to generate insights
4. **Fallback Analysis**: Provides basic analysis if LLM fails
5. **Structured Response**: Returns organized results

### LLM Integration

The application uses Hugging Face's free inference API with the DialoGPT-large model. If the API is unavailable, it falls back to keyword-based analysis.

## 🛠️ Development

### Project Structure

```
matchy-matchy/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── index.tsx       # React entry point
│   │   └── index.css       # Global styles
│   ├── public/
│   │   └── index.html      # HTML template
│   └── package.json        # Node.js dependencies
├── setup.sh               # Automated setup script
├── test_backend.py        # Backend testing script
└── README.md              # This file
```

### Adding Features

1. **Backend**: Add new endpoints in `backend/app.py`
2. **Frontend**: Modify components in `frontend/src/`
3. **Styling**: Use Tailwind CSS classes or add custom CSS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if port 5000 is available
- Verify Python dependencies are installed
- Ensure `.env` file exists with API key

**Frontend won't start:**
- Check if Node.js is installed
- Run `npm install` in the frontend directory
- Verify port 3000 is available

**Analysis fails:**
- Check your Hugging Face API key
- Verify the API key has proper permissions
- Check backend logs for error messages

**PDF upload issues:**
- Ensure the file is a valid PDF
- Check file size (should be under 10MB)
- Verify PDF is not password protected

### Getting Help

If you encounter issues:
1. Check the console logs in your browser
2. Review the backend terminal output
3. Run the test script: `python3 test_backend.py`
4. Verify your API key is working

## 🎉 Happy CV Analyzing!

This tool is designed to help you optimize your CV for specific job opportunities. Use the insights to tailor your application and increase your chances of landing your dream job! 