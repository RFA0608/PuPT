#include "./cpp/tcp_protocol_client.h"

#include <iostream>
#include <string>

#include "seal/seal.h"
#include <vector>

using namespace std;
using namespace seal;

const string host = "127.0.0.1";
const int port = 9999;

int main()
{
    tcp_client tccp = tcp_client(host, port);
    int poly_degree = -1;
    int plain_modulus = -1;
    poly_degree = tccp.Recv<int>();
    plain_modulus = tccp.Recv<int>();
    

    EncryptionParameters parms(scheme_type::bgv);
    size_t poly_modulus_degree = (size_t)poly_degree;
    parms.set_poly_modulus_degree(poly_modulus_degree);
    parms.set_coeff_modulus(CoeffModulus::BFVDefault(poly_modulus_degree));
    parms.set_plain_modulus(PlainModulus::Batching(poly_modulus_degree, plain_modulus));
    SEALContext context(parms);

    
    BatchEncoder batch_encoder(context);
    size_t slot_count = batch_encoder.slot_count();
    vector<int64_t> pod_matrix(slot_count, 0LL);
    Plaintext packed_data;
    batch_encoder.encode(pod_matrix, packed_data);
    int NoV = -1;

    NoV = tccp.Recv<int>();
    for(int i = 0; i < (int)slot_count; i++)
    {
        packed_data[i] = (int64_t)stoll(tccp.Recv<string>());
    }

    batch_encoder.decode(packed_data, pod_matrix);

    for(int i = 0; i < NoV; i++)
    {
        tccp.Send<string>(to_string(pod_matrix[i]));
    }

    return 0;
}