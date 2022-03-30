
#pragma once

#include <memory>
#include <fstream>
#include <map>
#include <boost/timer/timer.hpp>
#include <cassert>

namespace lapkt { namespace tools {

//! The Logger class uses a singleton and keeps track of time in order to timestamp the log messages.
class Logger {
protected:
	//! A map indexing all opened log streams
	std::map<std::string, std::ostream*> _streams;

	//! The directory where the log files will be written
	std::string _directory;

	//! The starting time, for reference
	boost::timer::cpu_timer _timer;

	//! The singleton object
	static std::unique_ptr<Logger> _instance;

	//! Basic version of the logging: returns a stream to write a message to the given filename
	std::ostream& log(const std::string& filename);

public:
	Logger(const std::string& directory);
	virtual ~Logger();

	//! We require explicit initizalition of the singleton object specifying the logging directory
	static void init(const std::string& directory);

	//! Retrieve the singleton instance, which has been previously initialized
	static Logger& instance();

	//! Returns a stream to debug to the given filename
	std::ostream& log(const std::string& level, const std::string& filename);

	//! Set the global singleton problem instance
	static void set_instance(std::unique_ptr<Logger>&& problem) {
		assert(!_instance);
		_instance = std::move(problem);
	}

	static std::unique_ptr<Logger>&& claim_ownership() {
		return std::move(_instance);
	}


};

} } // namespaces


// ************************
// THE ACTUAL LOGGING MACROS, WITH THREE DIFFERENT LOGGING LEVELS
// ************************
//! Info level
#define LPT_INFO(file, message) lapkt::tools::Logger::instance().log("INFO", file) << message << std::endl;

//! Debugging level
#ifdef DEBUG
#define LPT_DEBUG(file, message) lapkt::tools::Logger::instance().log("DEBUG", file) << message << std::endl;
#else
#define LPT_DEBUG(file, message)
#endif


//! Extreme Debugging level
#ifdef EDEBUG
#define LPT_EDEBUG(file, message) lapkt::tools::Logger::instance().log("EDEBUG", file) << message << std::endl;
#else
#define LPT_EDEBUG(file, message)
#endif
