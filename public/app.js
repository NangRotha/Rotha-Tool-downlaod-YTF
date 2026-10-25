// ==========================================================================
// RothaDownloader - Client Logic, CapCut Video Studio & Strict Bilingual Localization
// ==========================================================================

const TRANSLATIONS = {
  km: {
    // Header & Version
    badgePro: "PRO 4K",
    badgeVersion: "v២.៥",
    subtitle: "ឧបករណ៍ទាញយក និងកាត់តវីដេអូ YouTube, TikTok, Facebook សម្រាប់ Mac & Windows",
    statusReady: "ម៉ាស៊ីនរួចរាល់",
    statusError: "មិនទាន់ភ្ជាប់",
    btnStudio: "ស្ទូឌីយោកាត់ត",
    studioTitle: "ស្ទូឌីយោកាត់តវីដេអូ & AI",
    btnFolder: "ថតឯកសារ",
    openFolderTitle: "បើកថតឯកសារក្នុង Finder",
    btnInstallers: "ដំឡើង App",
    macInstallerTitle: "កម្មវិធីដំឡើងសម្រាប់ Mac (.DMG)",
    macInstallerDesc: "RothaDownloader.dmg (M1/M2/M3 & Intel)",
    winInstallerTitle: "កញ្ចប់កម្មវិធីសម្រាប់ Windows (.ZIP)",
    winInstallerDesc: "RothaDownloader-Windows.zip (Win 10/11)",
    supportedPlatforms: "គាំទ្រ:",

    // Input & Fetch
    inputPlaceholder: "បញ្ចូល ឬ Paste តំណភ្ជាប់ YouTube, TikTok, ឬ Facebook នៅទីនេះ...",
    pasteTitle: "Paste ពី Clipboard",
    btnPaste: "Paste",
    btnReset: "Reset",
    resetTitle: "សម្អាត និងចាប់ផ្ដើមថ្មី",
    btnFetch: "ទាញយកព័ត៌មាន",
    btnFetching: "កំពុងទាញយក...",
    quickTip: "គន្លឹះ: អាចទាញយកកម្រិត 4K (2160p), 1080p FHD, 720p HD ឬ បម្លែងទៅជា MP3 320kbps",
    selectQuality: "ជ្រើសរើសកម្រិតច្បាស់:",
    btnStartDownload: "ទាញយកឥឡូវនេះ",
    downloadingTitle: "កំពុងដំណើរការទាញយក...",

    // Download Stages & Status
    statusConnecting: "កំពុងភ្ជាប់ជាមួយម៉ាស៊ីនបម្រើ...",
    statusDownloading: "កំពុងទាញយកទិន្នន័យ...",
    statusMerging: "FFmpeg កំពុងបញ្ចូលរូបភាព និងសម្លេង (1080p/4K)...",
    statusConverting: "កំពុងបម្លែងទៅជា MP3 គុណភាពខ្ពស់...",
    statusOptimizing: "កំពុងកែសម្រួល Codec ឱ្យដំណើរការជាមួយ QuickTime Player (macOS)...",
    statusCompleted: "ការទាញយកបានបញ្ចប់ដោយជោគជ័យ! 🎉",
    statusFailed: "ការទាញយកបរាជ័យ",
    statSpeed: "ល្បឿន",
    statSize: "ទំហំ",
    statETA: "នៅសល់",

    // Actions
    btnPlay: "ចាក់វីដេអូ",
    btnReveal: "បើកក្នុង Finder",
    btnSaveDirect: "រក្សាទុកឯកសារ",
    btnNewDownload: "ទាញយកវីដេអូថ្មី",
    btnEdit: "កាត់តវីដេអូ",

    // History
    historyTitle: "ប្រវត្តិនៃការទាញយក",
    btnClearHistory: "សម្អាតប្រវត្តិ",
    noHistory: "មិនទាន់មានវីដេអូដែលបានទាញយកនៅឡើយទេ",
    footerText: "RothaDownloader • ដំណើរការដោយ yt-dlp & FFmpeg សម្រាប់ macOS & Windows • គុណភាពខ្ពស់ 4K & 1080p",

    // Settings
    settingsTitle: "ការកំណត់",
    folderSettingLabel: "ទីតាំងរក្សាទុកវីដេអូ:",
    btnOpen: "បើក",
    folderHelper: "លំនាំដើមគឺថត ~/Downloads នៅលើ Mac របស់អ្នក",
    cookiesSettingLabel: "ទាញយក Cookies ពី Browser (សម្រាប់វីដេអូ Private ឬ Facebook):",
    optNone: "គ្មាន (ទូទៅ - មិនប្រើ Cookies)",
    cookiesHelper: "បើកមុខងារនេះ ប្រសិនបើអ្នកចង់ទាញយកវីដេអូ Facebook ឬ YouTube ដែលទាមទារ Login",
    geminiSettingLabel: "Gemini API Key (ស្រេចចិត្ត - សម្រាប់ AI Subtitle & Viral Hook):",
    geminiHelper: "ប្រសិនបើមិនដាក់ កម្មវិធីនឹងប្រើម៉ាស៊ីន AI គំរូដែលភ្ជាប់មកស្រាប់ដោយឥតគិតថ្លៃ",
    lanAccessTitle: "ប្រើលើ Computer/Phone ផ្សេង",
    lanSettingLabel: "🌐 ប្រើនៅលើ Computer / Phone ផ្សេង (Wi-Fi Web Access):",
    lanHelper: "កុំព្យូទ័រ Laptop, iPhone, Android ឬ iPad ផ្សេងទៀតដែលភ្ជាប់ Wi-Fi ជាមួយគ្នានេះ អាចបើក Browser រួចវាយ Link ខាងលើដើម្បីប្រើភ្លាមៗ!",
    btnCopy: "ចម្លង Link",
    copiedLan: "បានចម្លង Link សម្រាប់ប្រើលើឧបករណ៍ផ្សេង!",
    btnCancel: "បោះបង់",
    btnSave: "រក្សាទុក",
    copiedToast: "បានចម្លង!",
    missingUrl: "សូមបញ្ចូលតំណភ្ជាប់វីដេអូជាមុនសិន។",

    // Features
    feat1Title: "កម្រិតច្បាស់ 4K & 1080p",
    feat1Desc: "ទាញយកវីដេអូកម្រិតខ្ពស់ 60fps ពី YouTube, TikTok & FB ជាមួយសម្លេងច្បាស់",
    feat2Title: "គ្មាន Watermark",
    feat2Desc: "TikTok គ្មាន Watermark & Facebook Reels ទាញយកផ្ទាល់បានលឿនបំផុត",
    feat3Title: "MP3 Audio 320kbps",
    feat3Desc: "បម្លែងវីដេអូទៅជាបទភ្លេង Original MP3 320kbps កម្រិត Studio Master",

    // CapCut Studio Translations
    studioHeading: "ស្ទូឌីយោកាត់តវីដេអូ & AI",
    studioSelectPrompt: "ជ្រើសរើសវីដេអូដើម្បីចាប់ផ្ដើមកាត់ត",
    trimTitle: "កាត់ប្រវែងវីដេអូ",
    trimStartLabel: "ពេលចាប់ផ្ដើម:",
    trimEndLabel: "ពេលបញ្ចប់:",
    btnSetCurrent: "យកពេលនេះ",
    speedTitle: "ល្បឿនវីដេអូ",
    tabEffects: "Effects & ពណ៌",
    tabCanvas: "ទំហំ Canvas",
    tabSubtitles: "AI Subtitle",
    tabAI: "AI ជំនួយ",
    filterPresetsTitle: "តម្រងពណ៌ CapCut:",
    filterNormal: "ធម្មតា",
    filterCinematic: "កុនភាពយន្ត",
    filterNeon: "ស៊ីប័រផាំង",
    filterVintage: "ភាពយន្តចាស់",
    filterBW: "សខ្មៅបែបបុរាណ",
    filterClarity: "ច្បាស់កម្រិត 4K",
    filterGlow: "ពន្លឺរលោង",
    adjustTitle: "កែតម្រូវលម្អិត:",
    sliderBrightness: "ពន្លឺ:",
    sliderContrast: "កម្រិតពណ៌:",
    sliderSaturation: "ដិតពណ៌:",
    canvasRatioTitle: "កម្រិតសមាមាត្រ Canvas:",
    aspectOrig: "ដើម (16:9)",
    aspectOrigDesc: "សមស្របសម្រាប់ YouTube & កុំព្យូទ័រ",
    aspect916: "បញ្ឈរ (9:16 TikTok / Reels)",
    aspect916Desc: "ប្លង់ទូរស័ព្ទ + ផ្ទៃខាងក្រោយព្រាលៗ",
    aspect11: "ការ៉េ (1:1)",
    aspect11Desc: "សមស្របសម្រាប់ Instagram & Post",
    btnGenSub: "បង្កើត Subtitle ដោយ AI",
    btnExportSrt: "ទាញយក .SRT",
    subStylesTitle: "ម៉ូដអក្សរ CapCut:",
    styleYellow: "អក្សរលឿង",
    styleWhite: "សស្អាត",
    styleNeon: "នេអុង",
    styleGold: "មាសរលើប",
    subListTitle: "បញ្ជីអត្ថបទ Subtitle:",
    btnAddLine: "+ បន្ថែមបន្ទាត់",
    emptySubNotice: "ចុចប៊ូតុង \"បង្កើត Subtitle ដោយ AI\" ឬបន្ថែមដោយដៃ",
    aiAssistTitle: "ជំនួយការ AI សម្រាប់វីដេអូ Viral:",
    aiHookTitle: "៥ Viral Hooks",
    aiHookDesc: "ចំណងជើងទាក់ទាញចិត្តនៅ ៣ វិនាទីដំបូង",
    aiCaptionTitle: "TikTok Caption & #Hashtags",
    aiCaptionDesc: "ការរៀបរាប់ និង hashtag ពេញនិយម",
    aiSummaryTitle: "សង្ខេបខ្លឹមសារវីដេអូ",
    aiSummaryDesc: "ចំណុចសំខាន់ៗដែលអ្នកទស្សនាចង់ដឹង",
    aiTranslateTitle: "បកប្រែ Script (KM ⇄ EN)",
    aiTranslateDesc: "បកប្រែជាភាសាខ្មែរ ឬអង់គ្លេសភ្លាមៗ",
    trimDurationLabel: "រយៈពេលកាត់ត:",
    quickTrim5sStart: "-5s ដើម",
    quickTrim5sEnd: "-5s ចុង",
    quickTrim15s: "15s Shorts",
    quickTrim30s: "30s Status",
    transformTitle: "ប្លង់ & ការបង្វិល:",
    btnFlipH: "ឆ្លុះឆ្វេងស្ដាំ (Mirror)",
    btnRotate90: "បង្វិល 90°",
    btnResetTransform: "ដើមវិញ",
    audioTitle: "សំឡេង & ល្បឿន:",
    sliderVolume: "កម្រិតសំឡេង:",
    toggleMute: "បិទសំឡេង",
    toggleFadeIn: "Fade In (1s)",
    toggleFadeOut: "Fade Out (1s)",
    btnResetAdjustments: "កំណត់ឡើងវិញ",
    exportResFormatLabel: "គុណភាព & ទម្រង់:",
    optExport1080p: "🎬 MP4 1080p FHD (ច្បាស់កម្រិតខ្ពស់)",
    optExport720p: "🎬 MP4 720p HD (ទំហំស្រាល)",
    optExport4k: "🎬 MP4 4K UHD (ច្បាស់អតិបរមា)",
    optExportMp3: "🎵 MP3 320kbps (ទាញយកតែសំឡេង Audio)",
    btnExportAudio: "នាំចេញតែសំឡេង (MP3)",
    btnExportVideo: "នាំចេញវីដេអូកាត់ត",
    exportingTitle: "កំពុងកាត់ត និង Render វីដេអូតាម FFmpeg...",
    exportComplete: "ការកាត់តបានជោគជ័យ! វីដេអូត្រូវបានរក្សាទុកក្នុង Downloads",
  },
  en: {
    // Header & Version
    badgePro: "PRO 4K",
    badgeVersion: "v2.5",
    subtitle: "YouTube • TikTok • Facebook Downloader & Video Studio for Mac & Windows",
    statusReady: "FFmpeg & yt-dlp Ready",
    statusError: "Disconnected",
    btnStudio: "Video Studio",
    studioTitle: "CapCut Video Studio & AI Assistant",
    btnFolder: "Downloads",
    openFolderTitle: "Open Downloads Folder",
    btnInstallers: "Install App",
    macInstallerTitle: "macOS Installer (.DMG)",
    macInstallerDesc: "RothaDownloader.dmg (M1/M2/M3 & Intel)",
    winInstallerTitle: "Windows Package (.ZIP)",
    winInstallerDesc: "RothaDownloader-Windows.zip (Win 10/11)",
    supportedPlatforms: "Supported:",

    // Input & Fetch
    inputPlaceholder: "Enter or paste YouTube, TikTok, or Facebook URL here...",
    pasteTitle: "Paste from Clipboard",
    btnPaste: "Paste",
    btnReset: "Reset",
    resetTitle: "Clear and Reset",
    btnFetch: "Fetch Info",
    btnFetching: "Fetching...",
    quickTip: "Tip: Download in 4K (2160p), 1080p FHD, 720p HD or extract MP3 at 320kbps",
    selectQuality: "Select Quality & Format:",
    btnStartDownload: "Download Now",
    downloadingTitle: "Downloading...",

    // Download Stages & Status
    statusConnecting: "Connecting to server...",
    statusDownloading: "Downloading video stream...",
    statusMerging: "Merging video & audio with FFmpeg (1080p/4K)...",
    statusConverting: "Extracting high-quality MP3 audio...",
    statusOptimizing: "Optimizing codecs for Apple QuickTime Player...",
    statusCompleted: "Download Complete! 🎉",
    statusFailed: "Download Failed",
    statSpeed: "Speed",
    statSize: "Size",
    statETA: "Remaining (ETA)",

    // Actions
    btnPlay: "Play Video",
    btnReveal: "Reveal in Folder",
    btnSaveDirect: "Save File",
    btnNewDownload: "Download Another Video",
    btnEdit: "Edit Video",

    // History
    historyTitle: "Download History",
    btnClearHistory: "Clear History",
    noHistory: "No downloaded videos yet.",
    footerText: "RothaDownloader • Powered by yt-dlp & FFmpeg for macOS & Windows • High Quality 4K & 1080p",

    // Settings
    settingsTitle: "Settings",
    folderSettingLabel: "Download Destination Folder:",
    btnOpen: "Open",
    folderHelper: "Defaults to ~/Downloads on your system",
    cookiesSettingLabel: "Extract Cookies from Browser (for Private / Facebook videos):",
    optNone: "None (Standard - no cookies)",
    cookiesHelper: "Enable this if downloading Facebook or YouTube videos that require your login session",
    geminiSettingLabel: "Gemini API Key (Optional - for AI Subtitles & Viral Engine):",
    geminiHelper: "If not provided, built-in offline smart AI models are used automatically for free.",
    lanAccessTitle: "Use on Other Computers/Phones",
    lanSettingLabel: "🌐 Use on Other Devices (Wi-Fi Web Access):",
    lanHelper: "Any other laptop, iPhone, Android, or iPad connected to the same Wi-Fi can open a browser and visit this URL to use RothaDownloader instantly!",
    btnCopy: "Copy Link",
    copiedLan: "Copied LAN Access URL to Clipboard!",
    btnCancel: "Cancel",
    btnSave: "Save Settings",
    copiedToast: "Pasted!",
    missingUrl: "Please enter a valid video URL first.",

    // Features
    feat1Title: "4K & 1080p Ultra HD",
    feat1Desc: "Download up to 4K 60fps from YouTube, TikTok & Facebook with crystal-clear audio",
    feat2Title: "No Watermark & Fast",
    feat2Desc: "TikTok No Watermark, Facebook Reels & Shorts instant high-speed download",
    feat3Title: "MP3 Audio 320kbps",
    feat3Desc: "Extract Studio-Master 320kbps MP3 audio directly from any video source",

    // CapCut Studio Translations
    studioHeading: "CapCut Video Studio & AI",
    studioSelectPrompt: "Select a video to start editing",
    trimTitle: "Trim & Cut Timeline",
    trimStartLabel: "Start Time:",
    trimEndLabel: "End Time:",
    btnSetCurrent: "Set Current",
    speedTitle: "Playback Speed",
    tabEffects: "Effects & Color",
    tabCanvas: "Canvas Ratio",
    tabSubtitles: "AI Subtitles",
    tabAI: "AI Assistant",
    filterPresetsTitle: "CapCut Color Presets:",
    filterNormal: "Original (Normal)",
    filterCinematic: "Cinematic Gold",
    filterNeon: "Cyberpunk Neon",
    filterVintage: "Vintage Film",
    filterBW: "Noir Black & White",
    filterClarity: "Crisp 4K Clarity",
    filterGlow: "Dreamy Glow",
    adjustTitle: "Fine Adjustments:",
    sliderBrightness: "Brightness:",
    sliderContrast: "Contrast:",
    sliderSaturation: "Saturation:",
    canvasRatioTitle: "Canvas Aspect Ratio:",
    aspectOrig: "Original (16:9 Widescreen)",
    aspectOrigDesc: "Perfect for YouTube & Desktop displays",
    aspect916: "Vertical (9:16 TikTok / Reels)",
    aspect916Desc: "Mobile full-screen with blurred background",
    aspect11: "Square (1:1 Instagram)",
    aspect11Desc: "Ideal for Instagram posts and feeds",
    btnGenSub: "Generate AI Subtitles",
    btnExportSrt: "Export .SRT",
    subStylesTitle: "CapCut Subtitle Styles:",
    styleYellow: "Yellow Bold",
    styleWhite: "Clean White",
    styleNeon: "Cyber Neon",
    styleGold: "Karaoke Gold",
    subListTitle: "Subtitle Cues List:",
    btnAddLine: "+ Add Cue",
    emptySubNotice: "Click \"Generate AI Subtitles\" or add cues manually.",
    aiAssistTitle: "AI Viral Video Assistant:",
    aiHookTitle: "5 Viral Hooks",
    aiHookDesc: "High-retention hooks for first 3 seconds",
    aiCaptionTitle: "TikTok Caption & #Hashtags",
    aiCaptionDesc: "Optimized descriptions & trending tags",
    aiSummaryTitle: "Video Summary & Key Points",
    aiSummaryDesc: "Bullet points and key takeaways",
    aiTranslateTitle: "Translate Script (KM ⇄ EN)",
    aiTranslateDesc: "Instant bilingual script translation",
    aiResultLabel: "AI Generated Output:",
    btnCopy: "Copy",
    trimDurationLabel: "Trim Duration:",
    quickTrim5sStart: "Skip 5s Start",
    quickTrim5sEnd: "Cut 5s End",
    quickTrim15s: "15s Shorts",
    quickTrim30s: "30s Status",
    transformTitle: "Transform & Orientation:",
    btnFlipH: "Mirror (Flip H)",
    btnRotate90: "Rotate 90°",
    btnResetTransform: "Reset",
    audioTitle: "Audio & Speed:",
    sliderVolume: "Volume Level:",
    toggleMute: "Mute Audio",
    toggleFadeIn: "Fade In (1s)",
    toggleFadeOut: "Fade Out (1s)",
    btnResetAdjustments: "Reset",
    exportResFormatLabel: "Format & Quality:",
    optExport1080p: "🎬 MP4 1080p FHD (High Quality)",
    optExport720p: "🎬 MP4 720p HD (Lightweight)",
    optExport4k: "🎬 MP4 4K UHD (Maximum Clarity)",
    optExportMp3: "🎵 MP3 320kbps (Audio Only)",
    btnExportAudio: "Export Audio (MP3)",
    btnExportVideo: "Export Edited Video",
    exportingTitle: "Rendering & Exporting Video with FFmpeg...",
    exportComplete: "Edit Complete! Video saved to your Downloads folder.",
  }
};

let currentLang = localStorage.getItem("rotha_lang") || "km";
let currentVideoInfo = null;
let selectedQuality = "1080p";
let currentDownloadId = null;
let pollTimer = null;
let lastDownloadedFilePath = null;

// ==========================================================================
// Khmer Numeral Helpers
// ==========================================================================
const KHMER_DIGITS = ['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩'];

function toKhmerDigits(val) {
  if (val === null || val === undefined) return "";
  return String(val).replace(/[0-9]/g, d => KHMER_DIGITS[d]);
}

function formatNumber(val, lang = currentLang) {
  if (lang === "km") {
    return toKhmerDigits(val);
  }
  return String(val);
}

function formatTime(seconds) {
  if (!seconds || isNaN(seconds)) seconds = 0;
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function t(key) {
  const dict = TRANSLATIONS[currentLang] || TRANSLATIONS.km;
  return dict[key] || key;
}

// ==========================================================================
// DOM Elements
// ==========================================================================
const urlInput = document.getElementById("urlInput");
const pasteBtn = document.getElementById("pasteBtn");
const resetBtn = document.getElementById("resetBtn");
const fetchBtn = document.getElementById("fetchBtn");
const fetchSpinner = document.getElementById("fetchSpinner");
const alertBox = document.getElementById("alertBox");
const alertMessage = document.getElementById("alertMessage");
const closeAlertBtn = document.getElementById("closeAlertBtn");

const detailsCard = document.getElementById("detailsCard");
const videoThumbnail = document.getElementById("videoThumbnail");
const videoDuration = document.getElementById("videoDuration");
const platformBadge = document.getElementById("platformBadge");
const videoTitle = document.getElementById("videoTitle");
const authorName = document.getElementById("authorName");
const maxResBadge = document.getElementById("maxResBadge");
const qualityGrid = document.getElementById("qualityGrid");
const startDownloadBtn = document.getElementById("startDownloadBtn");
const downloadBtnText = document.getElementById("downloadBtnText");

const progressCard = document.getElementById("progressCard");
const progressTitle = document.getElementById("progressTitle");
const progressStageBadge = document.getElementById("progressStageBadge");
const progressStatusDesc = document.getElementById("progressStatusDesc");
const progressPercentage = document.getElementById("progressPercentage");
const progressBarFill = document.getElementById("progressBarFill");
const progressPulse = document.getElementById("progressPulse");
const progressSpeed = document.getElementById("progressSpeed");
const progressSize = document.getElementById("progressSize");
const progressETA = document.getElementById("progressETA");
const successActions = document.getElementById("successActions");
const btnRevealFinder = document.getElementById("btnRevealFinder");
const btnPlayVideo = document.getElementById("btnPlayVideo");
const btnNewDownload = document.getElementById("btnNewDownload");

const historyList = document.getElementById("historyList");
const emptyHistoryNotice = document.getElementById("emptyHistoryNotice");
const historyCount = document.getElementById("historyCount");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");

const openDownloadsBtn = document.getElementById("openDownloadsBtn");
const settingsBtn = document.getElementById("settingsBtn");
const settingsModal = document.getElementById("settingsModal");
const closeSettingsBtn = document.getElementById("closeSettingsBtn");
const cancelSettingsBtn = document.getElementById("cancelSettingsBtn");
const saveSettingsBtn = document.getElementById("saveSettingsBtn");
const settingDownloadDir = document.getElementById("settingDownloadDir");
const settingBrowser = document.getElementById("settingBrowser");
const settingGeminiApiKey = document.getElementById("settingGeminiApiKey");
const settingOpenFolderBtn = document.getElementById("settingOpenFolderBtn");

const langToggle = document.getElementById("langToggle");
const langFlag = document.getElementById("langFlag");
const langText = document.getElementById("langText");
const versionBadge = document.getElementById("versionBadge");

const chipYT = document.getElementById("chipYT");
const chipTT = document.getElementById("chipTT");
const chipFB = document.getElementById("chipFB");

// Studio DOM Elements
const openStudioBtn = document.getElementById("openStudioBtn");
const studioModal = document.getElementById("studioModal");
const closeStudioBtn = document.getElementById("closeStudioBtn");
const btnCancelStudio = document.getElementById("btnCancelStudio");
const studioVideo = document.getElementById("studioVideo");
const studioSubOverlay = document.getElementById("studioSubOverlay");
const studioCanvasContainer = document.getElementById("studioCanvasContainer");
const studioVideoName = document.getElementById("studioVideoName");
const studioPlayBtn = document.getElementById("studioPlayBtn");
const studioPlayIcon = document.getElementById("studioPlayIcon");
const studioTimeDisplay = document.getElementById("studioTimeDisplay");
const studioScrubber = document.getElementById("studioScrubber");

const trimStartInput = document.getElementById("trimStartInput");
const trimEndInput = document.getElementById("trimEndInput");
const trimDurBadge = document.getElementById("trimDurBadge");
const btnSetStart = document.getElementById("btnSetStart");
const btnSetEnd = document.getElementById("btnSetEnd");
const btnQuickSkip5sStart = document.getElementById("btnQuickSkip5sStart");
const btnQuickCut5sEnd = document.getElementById("btnQuickCut5sEnd");
const btnQuickShorts15s = document.getElementById("btnQuickShorts15s");
const btnQuickStatus30s = document.getElementById("btnQuickStatus30s");

const btnFlipH = document.getElementById("btnFlipH");
const btnRotate90 = document.getElementById("btnRotate90");
const btnResetTransform = document.getElementById("btnResetTransform");
const badgeRotateDeg = document.getElementById("badgeRotateDeg");

const speedPills = document.querySelectorAll(".speed-pill");
const sliderVolume = document.getElementById("sliderVolume");
const valVolume = document.getElementById("valVolume");
const checkMuteAudio = document.getElementById("checkMuteAudio");
const checkFadeIn = document.getElementById("checkFadeIn");
const checkFadeOut = document.getElementById("checkFadeOut");

const studioTabBtns = document.querySelectorAll(".studio-tab-btn");
const studioTabContents = document.querySelectorAll(".studio-tab-content");

const filterCards = document.querySelectorAll(".filter-card");
const sliderBrightness = document.getElementById("sliderBrightness");
const sliderContrast = document.getElementById("sliderContrast");
const sliderSaturation = document.getElementById("sliderSaturation");
const valBrightness = document.getElementById("valBrightness");
const valContrast = document.getElementById("valContrast");
const valSaturation = document.getElementById("valSaturation");
const btnResetAdjustments = document.getElementById("btnResetAdjustments");

const aspectCards = document.querySelectorAll(".aspect-card");

const btnGenSubtitles = document.getElementById("btnGenSubtitles");
const btnExportSrt = document.getElementById("btnExportSrt");
const subStylesRow = document.getElementById("subStylesRow");
const subStyleChips = document.querySelectorAll(".sub-style-chip");
const subItemsList = document.getElementById("subItemsList");
const btnAddSubLine = document.getElementById("btnAddSubLine");

const btnAiHook = document.getElementById("btnAiHook");
const btnAiCaption = document.getElementById("btnAiCaption");
const btnAiSummary = document.getElementById("btnAiSummary");
const btnAiTranslate = document.getElementById("btnAiTranslate");
const aiResultCard = document.getElementById("aiResultCard");
const aiResultBody = document.getElementById("aiResultBody");
const btnCopyAiResult = document.getElementById("btnCopyAiResult");

const studioExportFormat = document.getElementById("studioExportFormat");
const btnExportVideo = document.getElementById("btnExportVideo");
const btnExportVideoText = document.getElementById("btnExportVideoText");
const studioStatusText = document.getElementById("studioStatusText");
const studioProgressWrap = document.getElementById("studioProgressWrap");
const studioProgressFill = document.getElementById("studioProgressFill");

// ==========================================================================
// Studio State
// ==========================================================================
let studioVideoPath = null;
let studioDuration = 0;
let studioSpeed = 1.0;
let studioFilter = "none";
let studioBrightnessVal = 100;
let studioContrastVal = 100;
let studioSaturationVal = 100;
let studioFlipH = false;
let studioFlipV = false;
let studioRotate = 0;
let studioVolumeVal = 100;
let studioMute = false;
let studioFadeIn = false;
let studioFadeOut = false;
let studioCanvas = "original";
let studioSubtitles = [];
let studioSubStyle = "yellow-bold";
let studioEditPollTimer = null;
let studioActiveEditId = null;

// ==========================================================================
// App Initialization
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  applyLanguage(currentLang);
  checkBackendStatus();
  loadHistory();
  loadSettings();
  setupEventListeners();
  setupStudioListeners();
});

function setupEventListeners() {
  // Language toggle
  langToggle.addEventListener("click", () => {
    currentLang = currentLang === "km" ? "en" : "km";
    localStorage.setItem("rotha_lang", currentLang);
    applyLanguage(currentLang);
    loadHistory(); // Re-render history with correct language numerals
  });

  // URL Input listener
  urlInput.addEventListener("input", () => {
    updatePlatformChips(urlInput.value);
  });

  urlInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      fetchVideoInfo();
    }
  });

  // Clipboard Paste button
  pasteBtn.addEventListener("click", async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text && text.trim().startsWith("http")) {
        urlInput.value = text.trim();
        updatePlatformChips(urlInput.value);
        fetchVideoInfo();
      } else {
        urlInput.focus();
      }
    } catch (e) {
      urlInput.focus();
    }
  });

  if (resetBtn) resetBtn.addEventListener("click", resetAll);
  if (btnNewDownload) btnNewDownload.addEventListener("click", resetAll);

  fetchBtn.addEventListener("click", fetchVideoInfo);
  closeAlertBtn.addEventListener("click", hideAlert);
  startDownloadBtn.addEventListener("click", startDownload);

  btnRevealFinder.addEventListener("click", () => {
    if (lastDownloadedFilePath) openFileInFinder(lastDownloadedFilePath);
  });

  btnPlayVideo.addEventListener("click", () => {
    if (lastDownloadedFilePath) playFile(lastDownloadedFilePath);
  });

  openDownloadsBtn.addEventListener("click", () => {
    openDownloadsFolder();
  });

  // Settings modal
  settingsBtn.addEventListener("click", () => {
    settingsModal.style.display = "flex";
  });
  closeSettingsBtn.addEventListener("click", () => {
    settingsModal.style.display = "none";
  });
  cancelSettingsBtn.addEventListener("click", () => {
    settingsModal.style.display = "none";
  });
  saveSettingsBtn.addEventListener("click", saveSettings);
  settingOpenFolderBtn.addEventListener("click", () => {
    openDownloadsFolder(settingDownloadDir.value);
  });

  const settingCopyLanBtn = document.getElementById("settingCopyLanBtn");
  if (settingCopyLanBtn) {
    settingCopyLanBtn.addEventListener("click", () => {
      const url = document.getElementById("settingLanUrl")?.value;
      if (url && url.startsWith("http")) {
        navigator.clipboard.writeText(url).then(() => {
          showAlert(t("copiedLan") || "Copied Link!");
        });
      }
    });
  }

  // Installers Dropdown Toggle
  const installDropdownWrapper = document.getElementById("installDropdownWrapper");
  const installMenuBtn = document.getElementById("installMenuBtn");
  if (installMenuBtn && installDropdownWrapper) {
    installMenuBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      installDropdownWrapper.classList.toggle("open");
    });
    document.addEventListener("click", (e) => {
      if (!installDropdownWrapper.contains(e.target)) {
        installDropdownWrapper.classList.remove("open");
      }
    });
  }

  const btnLanAccessDropdown = document.getElementById("btnLanAccessDropdown");
  if (btnLanAccessDropdown) {
    btnLanAccessDropdown.addEventListener("click", () => {
      const url = document.getElementById("settingLanUrl")?.value;
      if (url && url.startsWith("http")) {
        navigator.clipboard.writeText(url).then(() => {
          showAlert(`${t("copiedLan") || "Copied Link:"}\n${url}`);
        });
      } else {
        settingsModal.style.display = "flex";
      }
    });
  }

  clearHistoryBtn.addEventListener("click", clearHistory);
}

// ==========================================================================
// Reset All
// ==========================================================================
function resetAll() {
  urlInput.value = "";
  currentVideoInfo = null;
  currentDownloadId = null;
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
  if (detailsCard) detailsCard.style.display = "none";
  if (progressCard) progressCard.style.display = "none";
  if (successActions) successActions.style.display = "none";
  const featuresGrid = document.getElementById("featuresGrid");
  if (featuresGrid) featuresGrid.style.display = "grid";
  hideAlert();
  if (startDownloadBtn) startDownloadBtn.disabled = false;

  [chipYT, chipTT, chipFB].forEach(c => {
    if (c) c.classList.remove("active");
  });

  const urlPlatformIcon = document.getElementById("urlPlatformIcon");
  if (urlPlatformIcon) {
    urlPlatformIcon.innerHTML = `
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
      </svg>
    `;
    urlPlatformIcon.style.color = "var(--text-muted)";
  }

  if (btnPlayVideo) btnPlayVideo.style.display = "flex";
  if (btnRevealFinder) btnRevealFinder.style.display = "flex";
  const btnDownloadFile = document.getElementById("btnDownloadFile");
  if (btnDownloadFile) btnDownloadFile.style.display = "flex";

  urlInput.focus();
}

// ==========================================================================
// Language System & Strict Numeral Formatting
// ==========================================================================
function applyLanguage(lang) {
  const dict = TRANSLATIONS[lang] || TRANSLATIONS.km;

  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
    const key = el.getAttribute("data-i18n-title");
    if (dict[key]) {
      el.title = dict[key];
    }
  });

  if (lang === "km") {
    langFlag.textContent = "🇰🇭";
    langText.textContent = "ខ្មែរ";
    document.documentElement.lang = "km";
    if (versionBadge) versionBadge.textContent = "v២.៥";
  } else {
    langFlag.textContent = "🇺🇸";
    langText.textContent = "English";
    document.documentElement.lang = "en";
    if (versionBadge) versionBadge.textContent = "v2.5";
  }

  const backendStatusText = document.querySelector("#backendStatus .status-text");
  if (backendStatusText) {
    backendStatusText.textContent = t("statusReady");
  }

  updateDownloadBtnText();
}

function showAlert(msg) {
  alertMessage.textContent = msg;
  alertBox.style.display = "flex";
}

function hideAlert() {
  alertBox.style.display = "none";
}

function updatePlatformChips(url) {
  const lower = url.toLowerCase();
  chipYT.classList.remove("active");
  chipTT.classList.remove("active");
  chipFB.classList.remove("active");

  if (lower.includes("youtube.com") || lower.includes("youtu.be")) {
    chipYT.classList.add("active");
  } else if (lower.includes("tiktok.com")) {
    chipTT.classList.add("active");
  } else if (lower.includes("facebook.com") || lower.includes("fb.watch") || lower.includes("fb.com")) {
    chipFB.classList.add("active");
  }
}

// ==========================================================================
// Fetch Video Information
// ==========================================================================
async function fetchVideoInfo() {
  const url = urlInput.value.trim();
  if (!url) {
    showAlert(t("missingUrl"));
    urlInput.focus();
    return;
  }

  hideAlert();
  fetchBtn.disabled = true;
  fetchSpinner.style.display = "inline-block";
  document.querySelector("#fetchBtn .btn-text").textContent = t("btnFetching");

  try {
    const browser = settingBrowser.value || "none";
    const res = await fetch("/api/info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, browser }),
    });

    const data = await res.json();
    if (!res.ok || data.error) {
      throw new Error(data.error || "Failed to fetch video information.");
    }

    currentVideoInfo = data;
    renderVideoDetails(data);
  } catch (err) {
    showAlert(err.message);
  } finally {
    fetchBtn.disabled = false;
    fetchSpinner.style.display = "none";
    document.querySelector("#fetchBtn .btn-text").textContent = t("btnFetch");
  }
}

function renderVideoDetails(info) {
  if (!info) return;

  videoThumbnail.src = info.thumbnail || "";
  videoDuration.textContent = formatNumber(info.duration_formatted || "--:--");
  videoTitle.textContent = info.title || "Video";
  authorName.textContent = info.uploader || "Unknown";

  const rawPlatform = (info.platform || "video").toLowerCase();
  const platformName = rawPlatform.toUpperCase();
  platformBadge.textContent = platformName;
  if (rawPlatform === "youtube") {
    platformBadge.style.background = "#ff0033";
  } else if (rawPlatform === "tiktok") {
    platformBadge.style.background = "linear-gradient(135deg, #00f2fe, #fe0979)";
  } else if (rawPlatform === "facebook") {
    platformBadge.style.background = "#1877f2";
  } else {
    platformBadge.style.background = "#6366f1";
  }

  const maxHeight = info.max_height || 1080;
  if (maxHeight >= 2160) {
    maxResBadge.textContent = currentLang === "km" ? "៤K Ultra HD ✨" : "4K Ultra HD ✨";
    maxResBadge.style.background = "rgba(245, 158, 11, 0.2)";
    maxResBadge.style.color = "#fbbf24";
  } else if (maxHeight >= 1080) {
    maxResBadge.textContent = currentLang === "km" ? "១០៨០p Full HD 💎" : "1080p Full HD 💎";
    maxResBadge.style.background = "rgba(16, 185, 129, 0.2)";
    maxResBadge.style.color = "#34d399";
  } else if (maxHeight >= 720) {
    maxResBadge.textContent = currentLang === "km" ? "៧២០p HD" : "720p HD";
    maxResBadge.style.background = "rgba(56, 189, 248, 0.2)";
    maxResBadge.style.color = "#38bdf8";
  } else {
    maxResBadge.textContent = "Standard Quality";
    maxResBadge.style.background = "rgba(99, 102, 241, 0.15)";
    maxResBadge.style.color = "#a5b4fc";
  }

  // Quality pills
  qualityGrid.innerHTML = "";
  let defaultSet = false;

  const qualityOptions = (info.quality_options && Array.isArray(info.quality_options) && info.quality_options.length > 0)
    ? info.quality_options
    : [
        { id: "1080p", label: "Full HD (1080p)", resolution: "1920x1080", badge: "1080p FHD" },
        { id: "720p", label: "HD (720p)", resolution: "1280x720", badge: "720p HD" },
        { id: "mp3", label: "Audio Only (MP3 320kbps)", resolution: "Audio", badge: "MP3" }
      ];

  qualityOptions.forEach((opt, idx) => {
    const pill = document.createElement("div");
    pill.className = "quality-pill";
    pill.dataset.qualityId = opt.id;

    let badgeClass = "fhd";
    if (opt.id === "4k") badgeClass = "uhd";
    else if (opt.id === "mp3") badgeClass = "mp3";

    const labelFormatted = formatNumber(opt.label);
    const resFormatted = formatNumber(opt.resolution);

    pill.innerHTML = `
      <div class="pill-title">
        <span>${labelFormatted}</span>
        ${opt.badge ? `<span class="pill-badge ${badgeClass}">${formatNumber(opt.badge)}</span>` : ""}
      </div>
      <div class="pill-res">${resFormatted}</div>
    `;

    if (!defaultSet && (opt.id === "1080p" || (!qualityOptions.some(q => q.id === "1080p") && idx === 0))) {
      pill.classList.add("active");
      selectedQuality = opt.id;
      defaultSet = true;
    }

    pill.addEventListener("click", () => {
      document.querySelectorAll(".quality-pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      selectedQuality = opt.id;
      updateDownloadBtnText();
    });

    qualityGrid.appendChild(pill);
  });

  if (!defaultSet && qualityOptions.length > 0) {
    if (qualityGrid.children.length > 0) {
      qualityGrid.children[0].classList.add("active");
    }
    selectedQuality = qualityOptions[0].id;
  }

  updateDownloadBtnText();
  const featuresGrid = document.getElementById("featuresGrid");
  if (featuresGrid) featuresGrid.style.display = "none";
  detailsCard.style.display = "block";
  detailsCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function updateDownloadBtnText() {
  const rawLabel = selectedQuality ? selectedQuality.toUpperCase() : "1080P";
  const label = formatNumber(rawLabel);
  downloadBtnText.textContent = `${t("btnStartDownload")} (${label})`;
}

// ==========================================================================
// Download Execution & Real-time Tracking
// ==========================================================================
async function startDownload() {
  if (!currentVideoInfo) return;

  if (currentVideoInfo.is_cloud) {
    showAlert(
      currentLang === "km"
        ? "💡 អ្នកកំពុងប្រើប្រាស់លើ Vercel Cloud! មុខងារទាញយកវីដេអូកម្រិត 4K និងកាត់តដោយ FFmpeg Studio តម្រូវឱ្យដំណើរការលើ Desktop App ផ្ទាល់។ សូមចុច 'ដំឡើង App' នៅខាងលើដើម្បីទាញយក RothaDownloader សម្រាប់ Mac ឬ Windows ដោយឥតគិតថ្លៃ!"
        : "💡 You are using the Vercel Cloud Preview! Full 4K downloading & FFmpeg editing runs on your desktop. Click 'Install App' at the top to download RothaDownloader for Mac or Windows for free!"
    );
    return;
  }

  hideAlert();
  startDownloadBtn.disabled = true;

  progressCard.style.display = "block";
  successActions.style.display = "none";
  progressTitle.textContent = currentVideoInfo.title;

  if (progressStageBadge) {
    progressStageBadge.textContent = "CONNECTING";
    progressStageBadge.className = "stage-badge stage-connecting";
  }

  progressStatusDesc.textContent = t("statusConnecting");
  progressPercentage.textContent = formatNumber("1.0%");
  progressBarFill.style.width = "2%";
  progressBarFill.style.background = "var(--accent-gradient)";
  if (progressPulse) {
    progressPulse.style.background = "#6366f1";
    progressPulse.style.boxShadow = "0 0 10px #6366f1";
  }
  progressSpeed.textContent = "-- MB/s";
  progressSize.textContent = "-- MB";
  progressETA.textContent = "--:--";

  progressCard.scrollIntoView({ behavior: "smooth", block: "nearest" });

  try {
    const browser = settingBrowser.value || "none";
    const download_dir = settingDownloadDir.value.trim() || undefined;

    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: currentVideoInfo.webpage_url,
        quality: selectedQuality,
        browser,
        download_dir,
        video_info: currentVideoInfo,
      }),
    });

    const data = await res.json();
    if (!res.ok || data.error) {
      throw new Error(data.error || "Could not start download.");
    }

    currentDownloadId = data.download_id;

    if (pollTimer) clearInterval(pollTimer);
    pollTimer = setInterval(pollProgress, 200);
  } catch (err) {
    showAlert(err.message);
    startDownloadBtn.disabled = false;
  }
}

async function pollProgress() {
  if (!currentDownloadId) return;

  try {
    const res = await fetch(`/api/progress?id=${currentDownloadId}`);
    if (!res.ok) return;

    const task = await res.json();
    if (!task) return;

    const pct = task.percent || "0.0%";
    const pctNum = task.percent_num || 0;
    progressPercentage.textContent = formatNumber(pct);
    progressBarFill.style.width = `${Math.min(100, Math.max(2, pctNum))}%`;

    if (task.speed && task.speed !== "--") progressSpeed.textContent = formatNumber(task.speed);
    if (task.size && task.size !== "--") progressSize.textContent = formatNumber(task.size);
    if (task.eta && task.eta !== "--") progressETA.textContent = formatNumber(task.eta);

    if (progressStageBadge) {
      progressStageBadge.textContent = task.stage_badge || (task.stage ? task.stage.toUpperCase() : "DOWNLOADING");
      progressStageBadge.className = `stage-badge stage-${task.stage || "downloading"}`;
    }

    const statusDesc = currentLang === "km"
      ? (task.status_text_km || task.status_text || t("statusDownloading"))
      : (task.status_text_en || task.status_text || t("statusDownloading"));
    progressStatusDesc.textContent = statusDesc;

    if (task.completed) {
      clearInterval(pollTimer);
      pollTimer = null;
      startDownloadBtn.disabled = false;

      if (task.status === "completed") {
        if (progressStageBadge) {
          progressStageBadge.textContent = "COMPLETE";
          progressStageBadge.className = "stage-badge stage-completed";
        }
        progressStatusDesc.textContent = t("statusCompleted");
        progressBarFill.style.width = "100%";
        progressBarFill.style.background = "linear-gradient(135deg, #10b981, #059669)";
        progressPercentage.textContent = formatNumber("100%");

        if (progressPulse) {
          progressPulse.style.background = "#10b981";
          progressPulse.style.boxShadow = "0 0 14px #10b981";
        }

        lastDownloadedFilePath = task.filepath;
        const btnDownloadFile = document.getElementById("btnDownloadFile");
        if (btnDownloadFile && task.filepath) {
          btnDownloadFile.href = `/api/download-file?filepath=${encodeURIComponent(task.filepath)}`;
          btnDownloadFile.download = task.filename || "video.mp4";
        }
        successActions.style.display = "flex";
        loadHistory();
      } else {
        if (progressStageBadge) {
          progressStageBadge.textContent = "ERROR";
          progressStageBadge.className = "stage-badge stage-error";
        }
        progressStatusDesc.textContent = t("statusFailed");
        progressBarFill.style.background = "linear-gradient(135deg, #ef4444, #dc2626)";
        if (btnPlayVideo) btnPlayVideo.style.display = "none";
        if (btnRevealFinder) btnRevealFinder.style.display = "none";
        const btnDownloadFile = document.getElementById("btnDownloadFile");
        if (btnDownloadFile) btnDownloadFile.style.display = "none";
        successActions.style.display = "flex";
        showAlert(task.error || "Download encountered an error.");
      }
    }
  } catch (err) {
    console.error("Progress poll error:", err);
  }
}

// ==========================================================================
// History System
// ==========================================================================
async function loadHistory() {
  try {
    const res = await fetch("/api/history");
    const data = await res.json();
    const items = data.history || [];

    historyCount.textContent = formatNumber(items.length);

    if (items.length === 0) {
      emptyHistoryNotice.style.display = "flex";
      historyList.innerHTML = "";
      historyList.appendChild(emptyHistoryNotice);
      return;
    }

    emptyHistoryNotice.style.display = "none";
    historyList.innerHTML = "";

    items.forEach((item) => {
      const el = document.createElement("div");
      el.className = "history-item";

      const thumbUrl = item.thumbnail || "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2364748b'><path d='M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zm-10-7l-4 5h10l-3-4-2 2.5z'/></svg>";
      const formattedSize = formatNumber(item.size || "");
      const formattedDate = formatNumber(item.date_str || "");
      const formattedQuality = formatNumber(item.quality ? item.quality.toUpperCase() : "");

      el.innerHTML = `
        <img src="${thumbUrl}" class="history-thumb" alt="Thumbnail">
        <div class="history-meta">
          <div class="history-title" title="${item.title}">${item.title}</div>
          <div class="history-sub">
            <span class="history-quality-badge">${formattedQuality}</span>
            <span>${item.platform ? item.platform.toUpperCase() : ""}</span>
            <span>•</span>
            <span>${formattedSize}</span>
            <span>•</span>
            <span>${formattedDate}</span>
          </div>
        </div>
        <div class="history-actions">
          <!-- Edit Video with CapCut Studio Button -->
          <button class="btn-history-action btn-edit-action" title="${t("btnEdit")}">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="23 7 16 12 23 17 23 7"></polygon>
              <rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect>
            </svg>
          </button>
          <a class="btn-history-action" href="/api/download-file?filepath=${encodeURIComponent(item.filepath || '')}" download="${item.filename || 'video.mp4'}" title="${t("btnSaveDirect")}">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
          </a>
          <button class="btn-history-action btn-finder-action" title="${t("btnReveal")}">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
            </svg>
          </button>
          <button class="btn-history-action btn-play-action" title="${t("btnPlay")}">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
          </button>
        </div>
      `;

      // Studio Edit button click
      el.querySelector(".btn-edit-action").addEventListener("click", () => {
        if (item.filepath) {
          openCapCutStudio(item.filepath, item.title);
        }
      });

      el.querySelector(".btn-finder-action").addEventListener("click", () => {
        if (item.filepath) openFileInFinder(item.filepath);
      });

      el.querySelector(".btn-play-action").addEventListener("click", () => {
        if (item.filepath) playFile(item.filepath);
      });

      historyList.appendChild(el);
    });
  } catch (err) {
    console.error("Load history error:", err);
  }
}

async function openFileInFinder(filepath) {
  try {
    const res = await fetch("/api/open-file", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filepath }),
    });
    const data = await res.json();
    if (!res.ok) showAlert(data.error || "File could not be opened.");
  } catch (err) {
    showAlert("Cannot open Finder.");
  }
}

async function playFile(filepath) {
  try {
    const res = await fetch("/api/play-file", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filepath }),
    });
    const data = await res.json();
    if (!res.ok) showAlert(data.error || "Could not launch media player.");
  } catch (err) {
    showAlert("Cannot play file.");
  }
}

async function openDownloadsFolder(folder) {
  try {
    await fetch("/api/open-folder", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folder }),
    });
  } catch (err) {
    console.error(err);
  }
}

async function clearHistory() {
  const confirmMsg = currentLang === "km"
    ? "តើអ្នកពិតជាចង់សម្អាតប្រវត្តិទាញយកមែនទេ?"
    : "Are you sure you want to clear all download history?";
  if (confirm(confirmMsg)) {
    await fetch("/api/clear-history", { method: "POST" });
    loadHistory();
  }
}

// ==========================================================================
// Settings System
// ==========================================================================
async function loadSettings() {
  try {
    const res = await fetch("/api/settings");
    const data = await res.json();
    settingDownloadDir.value = data.download_dir || "";
    settingBrowser.value = data.browser || "none";
    if (settingGeminiApiKey) {
      settingGeminiApiKey.value = localStorage.getItem("rotha_gemini_key") || "";
    }
  } catch (err) {
    console.error(err);
  }
}

async function saveSettings() {
  try {
    if (settingGeminiApiKey) {
      localStorage.setItem("rotha_gemini_key", settingGeminiApiKey.value.trim());
    }
    const res = await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        download_dir: settingDownloadDir.value.trim(),
        browser: settingBrowser.value,
      }),
    });
    if (res.ok) {
      settingsModal.style.display = "none";
    }
  } catch (err) {
    showAlert("Failed to save settings.");
  }
}

async function checkBackendStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    if (data.ok) {
      if (data.is_cloud) {
        document.getElementById("backendStatus").innerHTML = `
          <span class="status-dot online" style="background:#38bdf8;box-shadow:0 0 8px #38bdf8"></span>
          <span class="status-text">${currentLang === "km" ? "Vercel Cloud • ភ្ជាប់ស្រេច" : "Vercel Cloud • Connected"}</span>
        `;
        return;
      }
      document.getElementById("backendStatus").innerHTML = `
        <span class="status-dot online"></span>
        <span class="status-text">${t("statusReady")}</span>
      `;
      if (data.lan_url) {
        const lanInput = document.getElementById("settingLanUrl");
        if (lanInput) lanInput.value = data.lan_url;
        const lanDesc = document.getElementById("lanUrlDropdownDesc");
        if (lanDesc) lanDesc.textContent = data.lan_url;
      }
    }
  } catch (err) {
    document.getElementById("backendStatus").innerHTML = `
      <span class="status-dot" style="background:#ef4444;box-shadow:0 0 8px #ef4444"></span>
      <span class="status-text" style="color:#fca5a5">${t("statusError")}</span>
    `;
  }
}

// ==========================================================================
// CapCut Video Studio & AI Assistant Implementation
// ==========================================================================
function setupStudioListeners() {
  // Top nav Studio Button
  if (openStudioBtn) {
    openStudioBtn.addEventListener("click", () => {
      if (lastDownloadedFilePath) {
        openCapCutStudio(lastDownloadedFilePath);
      } else {
        // Find latest from history
        fetch("/api/history")
          .then((r) => r.json())
          .then((d) => {
            if (d.history && d.history.length > 0) {
              openCapCutStudio(d.history[0].filepath, d.history[0].title);
            } else {
              showAlert(currentLang === "km" 
                ? "សូមទាញយកវីដេអូជាមុនសិន ឬចុចកាត់តនៅលើប្រវត្តិវីដេអូ!" 
                : "Please download a video first or select one from history to edit!");
            }
          });
      }
    });
  }

  // Close Studio Modal
  if (closeStudioBtn) closeStudioBtn.addEventListener("click", closeCapCutStudio);
  if (btnCancelStudio) btnCancelStudio.addEventListener("click", closeCapCutStudio);

  // Video playback
  if (studioPlayBtn) {
    studioPlayBtn.addEventListener("click", toggleStudioPlay);
  }

  studioVideo.addEventListener("play", () => {
    studioPlayIcon.innerHTML = `<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>`;
  });

  studioVideo.addEventListener("pause", () => {
    studioPlayIcon.innerHTML = `<polygon points="5 3 19 12 5 21 5 3"></polygon>`;
  });

  studioVideo.addEventListener("timeupdate", onStudioTimeUpdate);

  studioVideo.addEventListener("loadedmetadata", () => {
    studioDuration = studioVideo.duration || 0;
    studioScrubber.max = studioDuration;
    trimEndInput.value = studioDuration.toFixed(1);
    trimStartInput.value = "0.0";
    updateStudioTimeDisplay();
    updateTrimDurationBadge();
  });

  // Scrubber scrubbing
  studioScrubber.addEventListener("input", () => {
    studioVideo.currentTime = parseFloat(studioScrubber.value);
    updateStudioTimeDisplay();
  });

  // Trim duration updates
  trimStartInput.addEventListener("input", updateTrimDurationBadge);
  trimEndInput.addEventListener("input", updateTrimDurationBadge);

  // Trim current buttons
  if (btnSetStart) {
    btnSetStart.addEventListener("click", () => {
      trimStartInput.value = studioVideo.currentTime.toFixed(1);
      updateTrimDurationBadge();
    });
  }
  if (btnSetEnd) {
    btnSetEnd.addEventListener("click", () => {
      trimEndInput.value = studioVideo.currentTime.toFixed(1);
      updateTrimDurationBadge();
    });
  }

  // Quick Trim Shortcuts
  if (btnQuickSkip5sStart) {
    btnQuickSkip5sStart.addEventListener("click", () => {
      const cur = parseFloat(trimStartInput.value) || 0;
      trimStartInput.value = Math.min(studioDuration, cur + 5.0).toFixed(1);
      updateTrimDurationBadge();
    });
  }
  if (btnQuickCut5sEnd) {
    btnQuickCut5sEnd.addEventListener("click", () => {
      const cur = parseFloat(trimEndInput.value) || studioDuration;
      trimEndInput.value = Math.max(0, cur - 5.0).toFixed(1);
      updateTrimDurationBadge();
    });
  }
  if (btnQuickShorts15s) {
    btnQuickShorts15s.addEventListener("click", () => {
      trimStartInput.value = "0.0";
      trimEndInput.value = Math.min(15.0, studioDuration).toFixed(1);
      updateTrimDurationBadge();
    });
  }
  if (btnQuickStatus30s) {
    btnQuickStatus30s.addEventListener("click", () => {
      trimStartInput.value = "0.0";
      trimEndInput.value = Math.min(30.0, studioDuration).toFixed(1);
      updateTrimDurationBadge();
    });
  }

  // Transform Actions: Mirror & Rotate
  if (btnFlipH) {
    btnFlipH.addEventListener("click", () => {
      studioFlipH = !studioFlipH;
      btnFlipH.classList.toggle("active", studioFlipH);
      applyStudioFiltersPreview();
    });
  }
  if (btnRotate90) {
    btnRotate90.addEventListener("click", () => {
      studioRotate = (studioRotate + 90) % 360;
      if (badgeRotateDeg) badgeRotateDeg.textContent = `${studioRotate}°`;
      btnRotate90.classList.toggle("active", studioRotate !== 0);
      applyStudioFiltersPreview();
    });
  }
  if (btnResetTransform) {
    btnResetTransform.addEventListener("click", () => {
      studioFlipH = false;
      studioRotate = 0;
      if (btnFlipH) btnFlipH.classList.remove("active");
      if (btnRotate90) btnRotate90.classList.remove("active");
      if (badgeRotateDeg) badgeRotateDeg.textContent = "0°";
      applyStudioFiltersPreview();
    });
  }

  // Audio Controls & Fades
  if (sliderVolume) {
    sliderVolume.addEventListener("input", () => {
      studioVolumeVal = parseInt(sliderVolume.value);
      if (valVolume) valVolume.textContent = `${studioVolumeVal}%`;
      applyStudioFiltersPreview();
    });
  }
  if (checkMuteAudio) {
    checkMuteAudio.addEventListener("change", () => {
      studioMute = checkMuteAudio.checked;
      applyStudioFiltersPreview();
    });
  }
  if (checkFadeIn) {
    checkFadeIn.addEventListener("change", () => {
      studioFadeIn = checkFadeIn.checked;
    });
  }
  if (checkFadeOut) {
    checkFadeOut.addEventListener("change", () => {
      studioFadeOut = checkFadeOut.checked;
    });
  }

  // Speed pills
  speedPills.forEach((btn) => {
    btn.addEventListener("click", () => {
      speedPills.forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      studioSpeed = parseFloat(btn.dataset.speed);
      studioVideo.playbackRate = studioSpeed;
    });
  });

  // Tab switching
  studioTabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      studioTabBtns.forEach((b) => b.classList.remove("active"));
      studioTabContents.forEach((c) => c.classList.remove("active"));
      btn.classList.add("active");
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add("active");
    });
  });

  // Filters
  filterCards.forEach((card) => {
    card.addEventListener("click", () => {
      filterCards.forEach((c) => c.classList.remove("active"));
      card.classList.add("active");
      studioFilter = card.dataset.filter;
      applyStudioFiltersPreview();
    });
  });

  // Adjustment Sliders - Standard Digits (Prevent 900% Khmer font hook bug)
  [sliderBrightness, sliderContrast, sliderSaturation].forEach((slider) => {
    if (!slider) return;
    slider.addEventListener("input", () => {
      studioBrightnessVal = parseInt(sliderBrightness.value);
      studioContrastVal = parseInt(sliderContrast.value);
      studioSaturationVal = parseInt(sliderSaturation.value);

      valBrightness.textContent = `${studioBrightnessVal}%`;
      valContrast.textContent = `${studioContrastVal}%`;
      valSaturation.textContent = `${studioSaturationVal}%`;

      applyStudioFiltersPreview();
    });
  });

  // Reset Fine Adjustments
  if (btnResetAdjustments) {
    btnResetAdjustments.addEventListener("click", () => {
      studioBrightnessVal = 100;
      studioContrastVal = 100;
      studioSaturationVal = 100;
      sliderBrightness.value = 100;
      sliderContrast.value = 100;
      sliderSaturation.value = 100;
      valBrightness.textContent = "100%";
      valContrast.textContent = "100%";
      valSaturation.textContent = "100%";
      applyStudioFiltersPreview();
    });
  }

  // Export Format Change
  if (studioExportFormat) {
    studioExportFormat.addEventListener("change", () => {
      const isMp3 = studioExportFormat.value === "mp3";
      if (btnExportVideoText) {
        btnExportVideoText.textContent = isMp3 ? t("btnExportAudio") : t("btnExportVideo");
      }
    });
  }

  // Aspect Ratio Cards
  aspectCards.forEach((card) => {
    card.addEventListener("click", () => {
      aspectCards.forEach((c) => c.classList.remove("active"));
      card.classList.add("active");
      studioCanvas = card.dataset.aspect;
      applyStudioCanvasPreview();
    });
  });

  // Subtitle Styles
  subStyleChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      subStyleChips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      studioSubStyle = chip.dataset.style;
      applyStudioSubStylePreview();
    });
  });

  // AI Subtitle Generation
  if (btnGenSubtitles) {
    btnGenSubtitles.addEventListener("click", generateAiSubtitles);
  }

  // Add Subtitle Cue Line
  if (btnAddSubLine) {
    btnAddSubLine.addEventListener("click", () => {
      const cur = studioVideo.currentTime;
      studioSubtitles.push({
        start: cur,
        end: cur + 3.0,
        text: currentLang === "km" ? "បញ្ចូលអត្ថបទនៅទីនេះ..." : "Enter subtitle here...",
      });
      renderSubtitleEditor();
    });
  }

  // Export SRT
  if (btnExportSrt) {
    btnExportSrt.addEventListener("click", downloadSrtFile);
  }

  // AI Viral Assistant Actions
  if (btnAiHook) btnAiHook.addEventListener("click", () => requestAiAssistance("hooks"));
  if (btnAiCaption) btnAiCaption.addEventListener("click", () => requestAiAssistance("caption"));
  if (btnAiSummary) btnAiSummary.addEventListener("click", () => requestAiAssistance("summary"));
  if (btnAiTranslate) btnAiTranslate.addEventListener("click", () => requestAiAssistance("translate"));

  // Copy AI Result
  if (btnCopyAiResult) {
    btnCopyAiResult.addEventListener("click", () => {
      navigator.clipboard.writeText(aiResultBody.textContent).then(() => {
        btnCopyAiResult.textContent = t("copiedToast");
        setTimeout(() => {
          btnCopyAiResult.textContent = t("btnCopy");
        }, 1500);
      });
    });
  }

  // Export Video Button
  if (btnExportVideo) {
    btnExportVideo.addEventListener("click", startVideoExport);
  }
}

function updateTrimDurationBadge() {
  const startSec = Math.max(0, parseFloat(trimStartInput.value) || 0);
  let endSec = parseFloat(trimEndInput.value) || studioDuration;
  if (endSec <= startSec) endSec = studioDuration;
  const dur = Math.max(0, endSec - startSec);
  if (trimDurBadge) {
    trimDurBadge.textContent = `${dur.toFixed(1)}s`;
  }
}

function openCapCutStudio(filepath, title = "") {
  if (!filepath) return;
  studioVideoPath = filepath;

  const displayTitle = title || filepath.split("/").pop();
  studioVideoName.textContent = displayTitle;

  // Set streaming source with HTTP 206 partial content support
  studioVideo.src = `/api/stream-video?filepath=${encodeURIComponent(filepath)}`;
  studioVideo.playbackRate = studioSpeed;

  // Reset controls
  studioFilter = "none";
  filterCards.forEach((c) => c.classList.toggle("active", c.dataset.filter === "none"));

  studioBrightnessVal = 100;
  studioContrastVal = 100;
  studioSaturationVal = 100;
  sliderBrightness.value = 100;
  sliderContrast.value = 100;
  sliderSaturation.value = 100;
  valBrightness.textContent = "100%";
  valContrast.textContent = "100%";
  valSaturation.textContent = "100%";

  studioFlipH = false;
  studioRotate = 0;
  if (btnFlipH) btnFlipH.classList.remove("active");
  if (btnRotate90) btnRotate90.classList.remove("active");
  if (badgeRotateDeg) badgeRotateDeg.textContent = "0°";

  studioVolumeVal = 100;
  studioMute = false;
  if (sliderVolume) sliderVolume.value = 100;
  if (valVolume) valVolume.textContent = "100%";
  if (checkMuteAudio) checkMuteAudio.checked = false;
  if (checkFadeIn) checkFadeIn.checked = false;
  if (checkFadeOut) checkFadeOut.checked = false;

  studioCanvas = "original";
  aspectCards.forEach((c) => c.classList.toggle("active", c.dataset.aspect === "original"));
  applyStudioCanvasPreview();

  studioSubtitles = [];
  renderSubtitleEditor();
  applyStudioSubStylePreview();
  applyStudioFiltersPreview();
  updateTrimDurationBadge();

  studioStatusText.textContent = "";
  studioProgressWrap.style.display = "none";
  aiResultCard.style.display = "none";

  studioModal.style.display = "flex";
  studioVideo.play().catch(() => {});
}

function closeCapCutStudio() {
  studioVideo.pause();
  studioVideo.src = "";
  studioModal.style.display = "none";
  if (studioEditPollTimer) {
    clearInterval(studioEditPollTimer);
    studioEditPollTimer = null;
  }
}

function toggleStudioPlay() {
  if (studioVideo.paused) {
    studioVideo.play();
  } else {
    studioVideo.pause();
  }
}

function onStudioTimeUpdate() {
  const cur = studioVideo.currentTime || 0;
  studioScrubber.value = cur;
  updateStudioTimeDisplay();

  // Update live subtitle overlay
  let activeText = "";
  let activeIdx = -1;

  for (let i = 0; i < studioSubtitles.length; i++) {
    const cue = studioSubtitles[i];
    if (cur >= cue.start && cur <= cue.end) {
      activeText = cue.text;
      activeIdx = i;
      break;
    }
  }

  studioSubOverlay.textContent = activeText;

  // Highlight active cue row in editor
  const rows = subItemsList.querySelectorAll(".sub-item-row");
  rows.forEach((r, idx) => {
    r.classList.toggle("active-cue", idx === activeIdx);
  });
}

function updateStudioTimeDisplay() {
  const cur = studioVideo.currentTime || 0;
  const curStr = formatTime(cur);
  const durStr = formatTime(studioDuration);
  studioTimeDisplay.textContent = `${curStr} / ${durStr}`;
}

function applyStudioFiltersPreview() {
  const b = studioBrightnessVal / 100;
  const c = studioContrastVal / 100;
  const s = studioSaturationVal / 100;

  let filterStr = "";
  if (studioFilter === "none") {
    filterStr = `brightness(${b}) contrast(${c}) saturate(${s})`;
  } else if (studioFilter === "cinematic") {
    filterStr = `brightness(${b * 1.05}) contrast(${c * 1.15}) saturate(${s * 1.25}) sepia(0.2)`;
  } else if (studioFilter === "neon") {
    filterStr = `brightness(${b * 1.1}) contrast(${c * 1.3}) saturate(${s * 1.6}) hue-rotate(15deg)`;
  } else if (studioFilter === "vintage") {
    filterStr = `brightness(${b * 0.95}) contrast(${c * 1.1}) saturate(${s * 0.75}) sepia(0.4)`;
  } else if (studioFilter === "bw") {
    filterStr = `brightness(${b * 1.05}) contrast(${c * 1.35}) grayscale(1)`;
  } else if (studioFilter === "clarity") {
    filterStr = `brightness(${b * 1.05}) contrast(${c * 1.22}) saturate(${s * 1.12})`;
  } else if (studioFilter === "glow") {
    filterStr = `brightness(${b * 1.15}) contrast(${c * 1.05}) saturate(${s * 1.15}) drop-shadow(0 0 6px rgba(255,255,255,0.25))`;
  }

  studioVideo.style.filter = filterStr;
}

function applyStudioCanvasPreview() {
  studioCanvasContainer.classList.remove("ratio-916", "ratio-11");
  if (studioCanvas === "9:16") {
    studioCanvasContainer.classList.add("ratio-916");
  } else if (studioCanvas === "1:1") {
    studioCanvasContainer.classList.add("ratio-11");
  }
}

function applyStudioSubStylePreview() {
  studioSubOverlay.className = `studio-sub-overlay style-${studioSubStyle}`;
}

// Subtitles Generator & Editor
async function generateAiSubtitles() {
  if (!studioVideoPath) return;

  btnGenSubtitles.disabled = true;
  btnGenSubtitles.innerHTML = `<span>${currentLang === "km" ? "កំពុងវិភាគ AI..." : "AI Analyzing..."}</span>`;

  try {
    const res = await fetch("/api/generate-subtitles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filepath: studioVideoPath,
        url: currentVideoInfo ? currentVideoInfo.webpage_url : "",
        duration: studioDuration,
      }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to generate subtitles.");

    studioSubtitles = data.subtitles || [];
    renderSubtitleEditor();
  } catch (err) {
    showAlert(err.message);
  } finally {
    btnGenSubtitles.disabled = false;
    btnGenSubtitles.innerHTML = `
      <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
        <path d="M12 2l2.4 7.4L22 12l-7.6 2.6L12 22l-2.4-7.4L2 12l7.6-2.6L12 2z"/>
      </svg>
      <span>${t("btnGenSub")}</span>
    `;
  }
}

function renderSubtitleEditor() {
  if (studioSubtitles.length === 0) {
    subItemsList.innerHTML = `<div class="empty-sub-notice">${t("emptySubNotice")}</div>`;
    return;
  }

  subItemsList.innerHTML = "";

  studioSubtitles.forEach((cue, idx) => {
    const row = document.createElement("div");
    row.className = "sub-item-row";

    const startStr = formatTime(cue.start);
    const endStr = formatTime(cue.end);

    row.innerHTML = `
      <span class="sub-item-times" title="Click to seek">${startStr}-${endStr}</span>
      <input type="text" class="sub-item-text-input" value="${cue.text.replace(/"/g, '&quot;')}">
      <button class="btn-del-sub" title="Delete">&times;</button>
    `;

    row.querySelector(".sub-item-times").addEventListener("click", () => {
      studioVideo.currentTime = cue.start;
      studioVideo.play();
    });

    row.querySelector(".sub-item-text-input").addEventListener("input", (e) => {
      cue.text = e.target.value;
    });

    row.querySelector(".btn-del-sub").addEventListener("click", () => {
      studioSubtitles.splice(idx, 1);
      renderSubtitleEditor();
    });

    subItemsList.appendChild(row);
  });
}

function downloadSrtFile() {
  if (studioSubtitles.length === 0) {
    showAlert(currentLang === "km" ? "មិនទាន់មាន Subtitle នៅឡើយទេ!" : "No subtitles available to export!");
    return;
  }

  let srtContent = "";
  studioSubtitles.forEach((cue, idx) => {
    const sTime = formatSrtTimestamp(cue.start);
    const eTime = formatSrtTimestamp(cue.end);
    srtContent += `${idx + 1}\n${sTime} --> ${eTime}\n${cue.text}\n\n`;
  });

  const blob = new Blob([srtContent], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "subtitles.srt";
  a.click();
  URL.revokeObjectURL(url);
}

function formatSrtTimestamp(sec) {
  const ms = Math.floor((sec % 1) * 1000);
  const totalS = Math.floor(sec);
  const s = totalS % 60;
  const m = Math.floor(totalS / 60) % 60;
  const h = Math.floor(totalS / 3600);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
}

// AI Assistant
async function requestAiAssistance(action) {
  if (!studioVideoPath) return;

  aiResultCard.style.display = "flex";
  aiResultBody.textContent = currentLang === "km" ? "កំពុងដំណើរការ AI..." : "AI processing...";

  const apiKey = localStorage.getItem("rotha_gemini_key") || "";
  const allSubText = studioSubtitles.map((s) => s.text).join(" ");

  try {
    const res = await fetch("/api/ai-assist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action,
        title: studioVideoName.textContent,
        text: allSubText,
        lang: currentLang,
        api_key: apiKey,
      }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "AI generation failed.");

    aiResultBody.textContent = data.result || "No response.";
  } catch (err) {
    aiResultBody.textContent = "Error: " + err.message;
  }
}

// Video Export Execution
async function startVideoExport() {
  if (!studioVideoPath) return;

  btnExportVideo.disabled = true;
  studioProgressWrap.style.display = "block";
  studioProgressFill.style.width = "5%";
  studioStatusText.textContent = t("exportingTitle");

  const startSec = parseFloat(trimStartInput.value) || 0;
  let endSec = parseFloat(trimEndInput.value) || studioDuration;
  if (endSec <= startSec) endSec = studioDuration;

  const exportChoice = document.getElementById("studioExportFormat")?.value || "1080p";
  const exportFormat = exportChoice === "mp3" ? "mp3" : "mp4";
  const exportRes = exportChoice === "mp3" ? "original" : exportChoice;

  const payload = {
    source_path: studioVideoPath,
    trim_start: startSec,
    trim_end: endSec,
    speed: studioSpeed,
    canvas: studioCanvas,
    filter_preset: studioFilter,
    brightness: studioBrightnessVal,
    contrast: studioContrastVal,
    saturation: studioSaturationVal,
    flip_h: studioFlipH,
    flip_v: studioFlipV,
    rotate: studioRotate,
    volume: studioVolumeVal / 100.0,
    mute: studioMute,
    fade_in: studioFadeIn,
    fade_out: studioFadeOut,
    export_res: exportRes,
    export_format: exportFormat,
    subtitles: studioSubtitles,
    sub_style: studioSubStyle,
  };

  try {
    const res = await fetch("/api/edit-video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to start export.");

    studioActiveEditId = data.edit_id;

    if (studioEditPollTimer) clearInterval(studioEditPollTimer);
    studioEditPollTimer = setInterval(pollEditProgress, 500);
  } catch (err) {
    showAlert(err.message);
    btnExportVideo.disabled = false;
    studioProgressWrap.style.display = "none";
  }
}

async function pollEditProgress() {
  if (!studioActiveEditId) return;

  try {
    const res = await fetch(`/api/edit-status?id=${studioActiveEditId}`);
    if (!res.ok) return;

    const task = await res.json();
    if (!task) return;

    const pct = task.percent || 0;
    studioProgressFill.style.width = `${Math.min(100, Math.max(5, pct))}%`;
    studioStatusText.textContent = (currentLang === "km" ? task.status_text_km : task.status_text_en) || task.status_text;

    if (task.completed) {
      clearInterval(studioEditPollTimer);
      studioEditPollTimer = null;
      btnExportVideo.disabled = false;

      if (task.status === "completed") {
        studioProgressFill.style.width = "100%";
        studioStatusText.textContent = t("exportComplete");
        loadHistory();

        // Download trigger
        if (task.output_path) {
          const a = document.createElement("a");
          a.href = `/api/download-file?filepath=${encodeURIComponent(task.output_path)}`;
          a.download = task.filename || "edited_video.mp4";
          a.click();
        }
      } else {
        studioStatusText.textContent = "Error: " + (task.error || "Export failed.");
        showAlert(task.error || "Export failed.");
      }
    }
  } catch (err) {
    console.error("Poll edit error:", err);
  }
}
