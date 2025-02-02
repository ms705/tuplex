//--------------------------------------------------------------------------------------------------------------------//
//                                                                                                                    //
//                                      Tuplex: Blazing Fast Python Data Science                                      //
//                                                                                                                    //
//                                                                                                                    //
//  (c) 2017 - 2021, Tuplex team                                                                                      //
//  Created by Leonhard Spiegelberg first on 1/1/2021                                                                 //
//  License: Apache 2.0                                                                                               //
//--------------------------------------------------------------------------------------------------------------------//

#ifndef TUPLEX_PYTHONDATASET_H
#define TUPLEX_PYTHONDATASET_H

#include "../../core/include/Context.h"
#include <DataSet.h>
#include <boost/python.hpp>
#include <ErrorDataSet.h>
#include "PythonWrappers.h"

namespace tuplex {
    // wrappers hold the actual objects
    class PythonDataSet {
    private:
        DataSet *_dataset;

        // helper functions to convert dataset fast to python objects
        PyObject* resultSetToCPython(ResultSet* rs, size_t maxRowCount);

        // fast primitives
        PyObject* boolToCPython(ResultSet* rs, size_t maxRowCount);
        PyObject* i64ToCPython(ResultSet* rs, size_t maxRowCount);
        PyObject* f64ToCPython(ResultSet* rs, size_t maxRowCount);
        PyObject* strToCPython(ResultSet* rs, size_t maxRowCount);
        PyObject* anyToCPython(ResultSet* rs, size_t maxRowCount);

        PyObject* anyToCPythonWithPyObjects(ResultSet* rs, size_t maxRowCount);

        // simple numeric tuples
        PyObject* i64TupleToCPython(ResultSet* rs, size_t numTupleElements, size_t maxRowCount);
        PyObject* f64TupleToCPython(ResultSet* rs, size_t numTupleElements, size_t maxRowCount);

        // convert a flat tuple type fast to list of tuples
        PyObject* simpleTupleToCPython(ResultSet* rs, const python::Type& type, size_t maxRowCount);
    public:
        PythonDataSet(): _dataset(nullptr)  {}
        void wrap(DataSet *dataset) {
            _dataset = dataset;
        }

        PythonDataSet unique();

        /*!
         * add a map operator to the pipeline
         * @param lambda_code string representation of the code
         * @param pickled_code pickled version of the UDF (fallback mechanism)
         * @param closureObject holding info about globals
         * @return Dataset
         */
        PythonDataSet map(const std::string& lambda_code, const std::string& pickled_code, PyObject* closureObject=nullptr);

        /*!
         * add a filter operator to the pipeline
         * @param lambda_code string representation of the code
         * @param pickled_code pickled version of the supplied UDF (fallback mechanism)
         * @param closureObject holding info about globals
         * @return Dataset
         */
        PythonDataSet filter(const std::string& lambda_code, const std::string& pickled_code, PyObject* closureObject=nullptr);

        /*!
         * add a resolver operator to the pipeline. Must have same type as the preceding operator
         * @param exceptionCode exeption Code as number
         * @param lambda_code code for function to be executed
         * @param pickled_code pickled code for function for backup
         * @param closureObject holding info about globals
         * @return Dataset
         */
        PythonDataSet resolve(const int64_t exceptionCode, const std::string& lambda_code, const std::string& pickled_code, PyObject* closureObject=nullptr);

        boost::python::object collect();
        boost::python::object take(const int64_t numRows);
        void show(const int64_t numRows=-1);

        // DataFrame like operations
        PythonDataSet mapColumn(const std::string& column, const std::string& lambda_code, const std::string& pickled_code, PyObject* closureObject=nullptr);

        PythonDataSet withColumn(const std::string& column, const std::string& lambda_code, const std::string& pickled_code, PyObject* closureObject=nullptr);

        PythonDataSet selectColumns(boost::python::list L);

        PythonDataSet renameColumn(const std::string& oldName, const std::string& newName);

        PythonDataSet ignore(const int64_t exceptionCode);

        PythonDataSet join(const PythonDataSet& right, const std::string& leftKeyColumn, const std::string& rightKeyColumn,
                const std::string& leftPrefix, const std::string& leftSuffix, const std::string& rightPrefix, const std::string& rightSuffix);

        PythonDataSet leftJoin(const PythonDataSet& right, const std::string& leftKeyColumn, const std::string& rightKeyColumn,
                           const std::string& leftPrefix, const std::string& leftSuffix, const std::string& rightPrefix, const std::string& rightSuffix);

        PythonDataSet cache(bool storeSpecialized);

        PythonDataSet aggregate(const std::string& comb, const std::string& comb_pickled,
                                const std::string& agg, const std::string& agg_pickled,
                                const std::string& initial_value_pickled, PyObject* combClosureObject=nullptr, PyObject* aggclosureObject=nullptr);

        PythonDataSet aggregateByKey(const std::string& comb, const std::string& comb_pickled,
                                const std::string& agg, const std::string& agg_pickled,
                                const std::string& initial_value_pickled, boost::python::list columns);

        // returns list of strings or empty list
        boost::python::list columns();

        // returns list of types (according to typing object)
        // None for error
        boost::python::object types();

        /*!
         * expose exception counts of a specific operator!
         * returns dictionary with counts
         */
        boost::python::object exception_counts();

        void tocsv(const std::string &file_path,
              const std::string &lambda_code ="",
              const std::string &pickled_code = "",
              size_t fileCount=0,
              size_t shardSize=0,
              size_t limit=std::numeric_limits<size_t>::max(),
              const std::string& null_value="",
              boost::python::object header=boost::python::object());
    };

    /*!
     * encode primitive types in str. make sure char is a large enough allocated pointer!
     * @param type
     * @param typeStr
     * @return true if varlenfield encountered.
     */
    inline bool makeTypeStr(const python::Type& type, char* typeStr) {
        assert(typeStr);
        assert(type.isTupleType());
        auto numTupleElements = type.parameters().size();
        bool varLenField = false;
        for(unsigned i = 0; i < numTupleElements; ++i) {
            auto t = type.parameters()[i];
            if(t == python::Type::BOOLEAN)
                typeStr[i] = 'b';
            else if(t == python::Type::I64)
                typeStr[i] = 'i';
            else if(t == python::Type::F64)
                typeStr[i] = 'f';
            else if(t == python::Type::STRING) {
                typeStr[i] = 's';
                varLenField = true;
            }
            else
                throw std::runtime_error("unknown type encountered in fastMixedSimple transfer: " + t.desc());
        }

        return varLenField;
    }
}

#endif //TUPLEX_PYTHONDATASET_H