#ifndef __SIW_PLUS_PLANNER__
#define __SIW_PLUS_PLANNER__

#include <py_strips_prob.hxx>
#include <fwd_search_prob.hxx>
#include <novelty.hxx>
#include <novelty_partition.hxx>
#include <h_1.hxx>
#include <rp_heuristic.hxx>

#include <aptk/rp_iw.hxx>
#include <aptk/siw_plus.hxx>
#include <aptk/serialized_search.hxx>


using	aptk::agnostic::Fwd_Search_Problem;
using 	aptk::agnostic::H1_Heuristic;
using	aptk::agnostic::H_Add_Evaluation_Function;
using	aptk::agnostic::Relaxed_Plan_Heuristic;

using 	aptk::agnostic::Novelty;
using 	aptk::agnostic::Novelty_Partition;
using	aptk::search::novelty_spaces::RP_IW;
using	aptk::search::novelty_spaces::SIW_Plus;
using	aptk::search::Serialized_Search;

typedef		aptk::search::novelty_spaces::Node< aptk::State >	        IW_Node;
typedef         Novelty_Partition<Fwd_Search_Problem, IW_Node>                  H_Novel_Fwd;


typedef		H1_Heuristic<Fwd_Search_Problem, H_Add_Evaluation_Function>	H_Add_Fwd; 
typedef		Relaxed_Plan_Heuristic< Fwd_Search_Problem, H_Add_Fwd >		H_Add_Rp_Fwd;

typedef		RP_IW< Fwd_Search_Problem, H_Novel_Fwd, H_Add_Rp_Fwd >	        RP_IW_Fwd;
typedef		SIW_Plus< Fwd_Search_Problem >                                  SIW_Plus_Fwd;


class	SIW_Plus_Planner : public STRIPS_Problem
{
public:

	SIW_Plus_Planner( );
	SIW_Plus_Planner( std::string, std::string );
	virtual ~SIW_Plus_Planner();

	
	virtual void setup();
	void	solve();

	int		m_iw_bound;
	std::string	m_log_filename;
	std::string	m_plan_filename;

protected:
	
	float	do_search( SIW_Plus_Fwd& engine);

};

#endif
