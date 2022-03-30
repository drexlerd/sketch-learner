
#include <fs/core/utils/config.hxx>
#include <fs/core/fs_types.hxx>
#include <lapkt/tools/logging.hxx>

#include "memory"

namespace fs0 {

std::unique_ptr<Config> Config::_instance = nullptr;

void Config::init(const std::string& root, const std::unordered_map<std::string, std::string>& user_options) {
	if (_instance) throw std::runtime_error("Global configuration object already initialized");
	_instance = std::make_unique<Config>(root, user_options);
}

//! Retrieve the singleton instance, which has been previously initialized
Config& Config::instance() {
	if (!_instance) throw std::runtime_error("The global configuration object needs to be explicitly initialized before using it");
	return *_instance;
}

template <typename OptionType>
OptionType parseOption(const std::unordered_map<std::string, std::string>& user_options, const std::string& key, std::map<std::string, OptionType> allowed, const std::string& default_value) {
	std::string parsed;

	auto it = user_options.find(key);
	if (it != user_options.end()) { // The user specified an option value, which thus has priority
		parsed = it->second;
	} else {
		parsed = default_value;
	}
	auto it2 = allowed.find(parsed);
	if (it2 == allowed.end()) {
		throw std::runtime_error("Invalid configuration option for key " + key + ": " + parsed);
	}

	return it2->second;
}

Config::Config(const std::string& root, const std::unordered_map<std::string, std::string>& user_options)
	: _user_options(user_options)
{
	load(""); // Load the default options
}

void Config::load(const std::string& filename) {
//	_node_evaluation = parseOption<EvaluationT>(_root, _user_options, "evaluation", {
//		{"eager", EvaluationT::eager},
//		{"delayed", EvaluationT::delayed},
//		{"delayed_for_unhelpful", EvaluationT::delayed_for_unhelpful}}
//	);

	_succ_gen_type = parseOption<SuccessorGenerationStrategy>(_user_options, "successor_generation", {
		{"naive", SuccessorGenerationStrategy::naive},
		{"functional_aware", SuccessorGenerationStrategy::functional_aware},
		{"match_tree", SuccessorGenerationStrategy::match_tree},
		{"adaptive", SuccessorGenerationStrategy::adaptive}},
      "naive"
	);
}


std::ostream& Config::print(std::ostream& os) const {
	os << "[Planner config]" << std::endl;
	return os;
}




} // namespaces
