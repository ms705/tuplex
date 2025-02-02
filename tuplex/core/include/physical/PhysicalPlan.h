//--------------------------------------------------------------------------------------------------------------------//
//                                                                                                                    //
//                                      Tuplex: Blazing Fast Python Data Science                                      //
//                                                                                                                    //
//                                                                                                                    //
//  (c) 2017 - 2021, Tuplex team                                                                                      //
//  Created by Leonhard Spiegelberg first on 1/1/2021                                                                 //
//  License: Apache 2.0                                                                                               //
//--------------------------------------------------------------------------------------------------------------------//

#ifndef TUPLEX_PHYSICALPLAN_H
#define TUPLEX_PHYSICALPLAN_H

#include <logical/LogicalPlan.h>
#include "ResultSet.h"
#include "PhysicalStage.h"

namespace tuplex {
    class LogicalPlan;
    class PhysicalPlan;
    class PhysicalStage;

    class PhysicalPlan {
    private:
        // leaf stage (calls recursively predecessors!)
        PhysicalStage *_stage;
        size_t _num_stages; // used to generate stage numbers!

        /*!
         * creates multiple stages (linked to each other)
         * @return
         */
        PhysicalStage* splitIntoAndPlanStages();
        PhysicalStage* createStage(LogicalOperator* root,
                                   LogicalOperator* endNode,
                                   bool isRootStage,
                                   EndPointMode outMode);

        MessageHandler& _logger = Logger::instance().logger("PhysicalPlan");
        const Context& _context;

        IBackend* backend() const { return _context.backend(); }

        std::shared_ptr<HistoryServerConnector> _hs;

        // ---- OLD CODE -----
        // experimental: AWS backend
        LogicalPlan *_lp;
        LogicalPlan *_lpOriginal; // unoptimized original plan (needs to be around for printing out exceptions)
        void aws_execute();

        struct File2FilePipeline {
            std::string blockExecName;
            std::string writeCallbackName;
            std::string ir_code;

            // input uris
            std::vector<URI>    inputURIs;
            std::vector<size_t> inputSizes;

            // single output path??
            URI outputURI;


            // CSV stuff
            std::vector<std::string> inColumns;
            std::vector<std::string> outColumns;
        };

        File2FilePipeline planFile2FilePipeline(const std::vector<LogicalOperator*>& nodes, bool allowUndefinedBehavior);
        void executeFile2FilePipelineViaLambda(const File2FilePipeline& pip);
        void executeWithParts(const tuplex::PhysicalPlan::File2FilePipeline &pip);
        double aggregateSamplingTime() const;
    public:

        PhysicalPlan(LogicalPlan* optimizedPlan, LogicalPlan* originalPlan, const Context& context);

        ~PhysicalPlan();

        /*!
         * gets the current context object.
         * @returns address to Context object.
         */
        const Context& getContext() const {
            return _context;
        }

        void execute();

        std::shared_ptr<ResultSet> resultSet();

        /*!
         * checks whether PhysicalPlan is valid or any errors occured
         * @return
         */
        bool good() { return _stage; }


        // static identifiers
        static std::string csvWriteCallbackName() { return "csvWriter"; }

        const LogicalPlan* logicalPlan() const { return _lp; }

        nlohmann::json getStagedRepresentationAsJSON() const;

        /*!
         * return the id of the final stage (i.e. the one with the final sink!) ==> @TODO: can there be more than one?
         * currently not, because action triggers job so all good...
         */
        int64_t lastStageID() const { return _stage->getID(); }

        std::string actionName() const;

        void foreachStage(std::function<void(const PhysicalStage*)> func) const;
    };
}

#endif //TUPLEX_PHYSICALPLAN_H