//--------------------------------------------------------------------------------------------------------------------//
//                                                                                                                    //
//                                      Tuplex: Blazing Fast Python Data Science                                      //
//                                                                                                                    //
//                                                                                                                    //
//  (c) 2017 - 2021, Tuplex team                                                                                      //
//  Created by Leonhard Spiegelberg first on 1/1/2021                                                                 //
//  License: Apache 2.0                                                                                               //
//--------------------------------------------------------------------------------------------------------------------//

#include <iostream>
#include <Pipe.h>
#include <boost/process.hpp>
#include <boost/algorithm/string.hpp>
#include <Logger.h>
#include <fstream>
#include <cstdlib>

int Pipe::pipe(const std::string& file_input) {

    try {

        using namespace boost::process;

        ipstream pipe_stdout;
        ipstream pipe_stderr;

        assert(_command.length() > 0);

        // get the program name
        auto idx = _command.find(' ');
        if(std::string::npos == idx)
            idx = _command.length();
        std::string name = _command.substr(0, idx);
        std::string tail = _command.substr(idx);

        std::string cmd = boost::process::search_path(name).generic_string() + tail;

        // check if file input is active, if so create a temp file
        if(file_input.length() > 0) {
            // @TODO: global temp dir should be used...
            // needs to be a configurable option...

            // deprecated
            // @TODO
            std::string tmppath = std::tmpnam(nullptr);
            std::ofstream ofs(tmppath + ".py");
            ofs<<file_input;
            ofs.close();
            cmd += " " + tmppath + ".py";
        }

        child c(cmd, std_err > pipe_stderr, std_out > pipe_stdout);

        std::string line;
        while (pipe_stdout && std::getline(pipe_stdout, line) && !line.empty()) {
            _stdout += line + "\n";
        }
        while (pipe_stderr && std::getline(pipe_stderr, line) && !line.empty()) {
            _stderr += line + "\n";
        }

        c.wait();
        _retval = c.exit_code();

    } catch(std::exception& e) {
        Logger::instance().logger("pipe").error(std::string("error while calling external process: ") + e.what());
        _retval = 1;
    }


    _executed = true;
    return retval();
}