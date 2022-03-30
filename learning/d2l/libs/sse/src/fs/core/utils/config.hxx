
#pragma once

#include <stdexcept>
#include <memory>
#include <unordered_map>
#include <boost/property_tree/ptree.hpp>
#include <fs/core/utils/lexical_cast.hxx>


namespace fs0 {

class MissingOption : public std::runtime_error {
public:
	MissingOption(const std::string& name) : std::runtime_error("Missing or Wrong option type: '" + name + "'") {}
};


//! A (singleton) object to load and store different planner configuration objects
class Config {
public:
	//! The type of relaxed plan extraction
	enum class RPGExtractionType {Propositional, Supported};

	//! The possible types of CSP resolutions we consider
	enum class CSPResolutionType {Full, Approximate};

	//! The CSP value selection heuristic
	enum class ValueSelection {MinVal, MinHMax};

	//! The type of support sets that should be given priority
	enum class SupportPriority {First, MinHMaxSum};

	//! The type of node evaluation
	enum class EvaluationT {eager, delayed, delayed_for_unhelpful};

	//! The type of successor generator to use
	enum class SuccessorGenerationStrategy { naive, functional_aware, match_tree, adaptive };

	//! Explicit initizalition of the singleton
	static void init(const std::string& root, const std::unordered_map<std::string, std::string>& user_options);

	//! Retrieve the singleton instance, which has been previously initialized
	static Config& instance();

	//! Prints a representation of the object to the given stream.
	friend std::ostream& operator<<(std::ostream &os, const Config& o) { return o.print(os); }
	std::ostream& print(std::ostream& os) const;

protected:
	static std::unique_ptr<Config> _instance;

	boost::property_tree::ptree _root;

	const std::unordered_map<std::string, std::string> _user_options;

	SuccessorGenerationStrategy	_succ_gen_type;

public:
	Config(const std::string& root, const std::unordered_map<std::string, std::string>& user_options);

	Config(const Config& other) = delete;
	~Config() = default;

	void load(const std::string& filename);

	SuccessorGenerationStrategy getSuccessorGeneratorType() const { return _succ_gen_type; }

	bool validate() const { return getOption("validate", false); }

	//! A generic getter
	template <typename T>
	T getOption(const std::string& key) const {
		auto it = _user_options.find(key);
		try {
			if (it != _user_options.end()) { // The user specified an option value, which thus has priority
				return boost::lexical_cast<T>(it->second);
			} else {
				return _root.get<T>(key);
			}
		} catch (const std::runtime_error& e) {
			throw MissingOption(key);
		}
	}

	template <typename T>
	T getOption(const std::string& key, const T& def) const {
		try {
			return getOption<T>(key);
		} catch (const MissingOption& e) {
			return def;
		}
	}

	// Partial specialization
	bool getOption(const std::string& key) const { return getOption<bool>(key); }
	bool getOption(const std::string& key, bool def) const { return getOption<bool>(key, def); }
};

} // namespaces
