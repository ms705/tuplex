//--------------------------------------------------------------------------------------------------------------------//
//                                                                                                                    //
//                                      Tuplex: Blazing Fast Python Data Science                                      //
//                                                                                                                    //
//                                                                                                                    //
//  (c) 2017 - 2021, Tuplex team                                                                                      //
//  Created by Leonhard Spiegelberg first on 1/1/2021                                                                 //
//  License: Apache 2.0                                                                                               //
//--------------------------------------------------------------------------------------------------------------------//

#ifdef BUILD_WITH_AWS
#ifndef TUPLEX_AWSCOMMON_H
#define TUPLEX_AWSCOMMON_H

#include <string>
#include <unordered_map>
#include <cstdlib>
#include <vector>

namespace tuplex {

    struct AWSCredentials {
        std::string access_key;
        std::string secret_key;

        static AWSCredentials get();
    };

    /*!
     * initializes AWS SDK globally (lazy)
     * @return true if initializing, else false
     */
    extern bool initAWS(const AWSCredentials& credentials, bool requesterPay=false);

}

// Amazon frequently changes the parameters of lambda functions,
// this here are a couple constants to update them
// current state: https://aws.amazon.com/about-aws/whats-new/2020/12/aws-lambda-supports-10gb-memory-6-vcpu-cores-lambda-functions/#:~:text=Events-,AWS%20Lambda%20now%20supports%20up%20to%2010%20GB%20of%20memory,vCPU%20cores%20for%20Lambda%20Functions&text=AWS%20Lambda%20customers%20can%20now,previous%20limit%20of%203%2C008%20MB.
// cf. https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
#define AWS_MINIMUM_LAMBDA_MEMORY_MB 128ul
// how much memory a function for Tuplex should have
#define AWS_MINIMUM_TUPLEX_MEMORY_REQUIREMENT_MB 384ul
#define AWS_MAXIMUM_LAMBDA_MEMORY_MB 10240ul
// note(Leonhard): I think the number of available cores/threads is dependent on the memory size
#define AWS_MAXIMUM_LAMBDA_THREADS 6

// the 64MB increase limit seems to have been changed now...

#endif //TUPLEX_AWSCOMMON_H
#endif