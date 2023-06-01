/**
 * @file XmlRecorder.h
 *
 * @ingroup Simulator/Recorders
 *
 * @brief An implementation for recording spikes history on xml file
 *
 * The XmlRecorder provides a mechanism for recording neuron's layout, spikes history,
 * and compile history information on xml file:
 *     -# neuron's locations, and type map,
 *     -# individual neuron's spike rate in epochs,
 *     -# network wide spike count in 10ms bins.
 */

#pragma once
#include "Global.h"
#include "Recorder.h"
#include "Model.h"
#include <fstream>
#include <vector>

class XmlRecorder : public Recorder {
public:
   // constructor which opens the xml file to store results
   XmlRecorder();

   static Recorder *Create()
   {
      return new XmlRecorder();
   }

   /// Initialize data in the newly loadeded xml file
   virtual void init() override;

   /// Init radii and rates history matrices with default values
   virtual void initDefaultValues() override;

   /// Init radii and rates history matrices with current radii and rates
   virtual void initValues() override;

   /// Get the current radii and rates vlaues
   virtual void getValues() override;

   /// Terminate process
   virtual void term() override;

   /// Compile history information in every epoch
   /// @param[in] vertices   The entire list of vertices.
   virtual void compileHistories(AllVertices &vertices) override;

   /// Writes simulation results to an output destination.
   /// @param  vertices the Vertex list to search from.
   virtual void saveSimData(const AllVertices &vertices) override;

   ///  Prints out all parameters to logging file.
   ///  Registered to OperationManager as Operation::printParameters
   virtual void printParameters() override;

   /// Store the neuron number and all the events for this neuron that registered in the variable owner class
   void registerVariables(string varName, EventBuffer &recordVar) override;

protected:
   // a signle neuron number
   string neuronName;

   // all events for a single neuron
   EventBuffer *singleNeuronEvents_;

   // history of accumulated event of a neurons
   std::vector<uint64_t> single_neuron_History_;

   // // create a structure contains the information of a variable
   // struct variableInfo{
   //    string variableName;
   //    EventBuffer* variableLocation;
   // };

   // // create table
   // std::vector<variableInfo> variableTable;


   // a file stream for xml output
   ofstream resultOut_;

   virtual string toXML(string name, vector<uint64_t> single_nueron_buffer) const;

   //this method will be deleted
   void getStarterNeuronMatrix(VectorMatrix &matrix, const std::vector<bool> &starterMap);
};
