package msg

const (
	DevUrl  = "https://localhost:8000/"
	BetaUrl = "https://dev.snapshot.lieber.men"
	ProdUrL = "https://snapshot.lieber.men"

	ServiceName     = "Snapshot"
	emoji           = "📸"
	prefix          = ServiceName + " " + emoji + ": "
	prefixMultiLine = ServiceName + " " + emoji

	HowToStart             = prefix + "Text START to play."
	EnterUsername          = prefix + "Text STOP to unsubscribe.\n\nPlease enter your username:"
	EnterUsernameAgain     = prefix + "please enter your username:"
	ConfirmUsername        = prefix + "You entered %s, text YES to confirm or NO to change."
	BadUsername            = prefix + "Username is invalid. Must be less than 16 characters and contain only letters, numbers, and underscores. Please try again:"
	RegistrationSuccessful = prefix + "You've successfully registered as %s. Thanks! :)"
	Prompt                 = prefixMultiLine + "\n\n✨%s✨\n\nSTOP to unsubscribe."

	InvalidUser      = prefix + "Couldn't find user, please register first."
	AlreadySubmitted = prefix + "You already submitted for this prompt."
	FailedPicSave    = prefix + "Couldn't save your pic, oops!"

	ViewSubmissions = prefix + "Thanks for submitting! View all submissions here:\n%s"
)
