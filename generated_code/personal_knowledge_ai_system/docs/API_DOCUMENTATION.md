# Personal Knowledge AI System
**Version**: 1.0.0
**Generated**: 2025-12-22 15:11:54

---

## Architecture Overview

- **Total Domains**: 6
- **Total Classes**: 30
- **Total Relationships**: 22

## Domains

### User Interface Domain
**Key Letter**: UID

No description

**Classes in User Interface Domain**:
- 🔄 **Message**: Merepresentasikan pesan dalam chat antara user dan AI.
- 📦 **ChatView**: Komponen UI utama untuk menampilkan chat.
- 📦 **ApiClient**: Menangani komunikasi HTTP ke backend.

### Ingestion Domain
**Key Letter**: ING

No description

**Classes in Ingestion Domain**:
- 🔄 **IngestionJob**: Merepresentasikan job untuk memproses data yang diingest.
- 📦 **IngestController**: API endpoint untuk menerima data.
- 📦 **IngestService**: Service untuk memvalidasi dan memproses data yang diingest.
- 📦 **MessageQueue**: Message queue untuk mengelola job.

### Extraction Domain
**Key Letter**: EXT

No description

**Classes in Extraction Domain**:
- 🔄 **ExtractionResult**: Hasil dari proses ekstraksi teks.
- 📦 **ExtractionWorker**: Worker yang memproses job ekstraksi.
- 📦 **ExtractionFactory**: Factory untuk memilih strategy ekstraksi yang tepat.
- 📦 **PdfExtractor**: Strategy untuk ekstraksi PDF.
- 📦 **OcrExtractor**: Strategy untuk ekstraksi gambar dengan OCR.
- 📦 **AudioTranscriber**: Strategy untuk transkripsi audio.

### Storage Domain
**Key Letter**: STR

No description

**Classes in Storage Domain**:
- 📦 **StorageService**: Service untuk menyimpan dokumen yang telah diekstrak.
- 📦 **EmbeddingGenerator**: Generator untuk membuat vector embedding dari teks.
- 📦 **VectorClient**: Client untuk berinteraksi dengan vector database.
- 📦 **MetadataClient**: Client untuk menyimpan metadata dokumen.

### AI Core Domain
**Key Letter**: AIC

No description

**Classes in AI Core Domain**:
- 🔄 **Answer**: Jawaban yang dihasilkan oleh AI untuk query pengguna.
- 📦 **QueryController**: Controller untuk menangani query pengguna.
- 📦 **RAGService**: Service untuk mengorkestrasi proses RAG.
- 📦 **DocumentRetriever**: Retriever untuk mencari dokumen relevan.
- 📦 **PromptBuilder**: Builder untuk menyusun prompt RAG.
- 📦 **LLMClient**: Client untuk berkomunikasi dengan Large Language Model.

### Proactive Analysis Domain
**Key Letter**: PAD

No description

**Classes in Proactive Analysis Domain**:
- 🔄 **Insight**: Insight yang dihasilkan dari analisis proaktif.
- 📦 **ProactiveWorker**: Worker yang menjalankan analisis proaktif terjadwal.
- 📦 **AnalysisEngine**: Mesin yang menjalankan berbagai strategi analisis.
- 📦 **NotificationService**: Service untuk mengirim notifikasi insight ke pengguna.
- 📦 **IAnalysisStrategy**: Interface untuk strategi analisis (e.g., ConnectionFinder).
- 📦 **ConnectionFinder**: Implementasi strategi untuk menemukan koneksi antar dokumen.
- 📦 **GapDetector**: Implementasi strategi untuk mendeteksi kesenjangan pengetahuan.

---

## Class Reference

### Message

**Type**: class

Merepresentasikan pesan dalam chat antara user dan AI.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `MessageID` | uuid | - |
| `Content` | string | - |
| `Sender` | string | - |
| `Timestamp` | datetime | - |
| `Type` | string | - |
| `Status` | state | - |

**Methods**:

- `userclickssend()`: Transition from *Draft* to *Sending*
- `apicallsuccess()`: Transition from *Sending* to *Sent*
- `networkerror()`: Transition from *Sending* to *Failed*
- `retry()`: Transition from *Failed* to *Sending*
- `serverconfirms()`: Transition from *Sent* to *Delivered*
- `userviews()`: Transition from *Delivered* to *Read*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### ChatView

**Type**: passive_class

Komponen UI utama untuk menampilkan chat.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ViewID` | uuid | - |
| `UserID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### ApiClient

**Type**: passive_class

Menangani komunikasi HTTP ke backend.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ClientID` | uuid | - |
| `BaseUrl` | string | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### IngestionJob

**Type**: class

Merepresentasikan job untuk memproses data yang diingest.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `JobID` | uuid | - |
| `DataType` | string | - |
| `SourceUri` | string | - |
| `UserID` | uuid | - |
| `RetryCount` | integer | - |
| `Status` | state | - |

**Methods**:

- `addtoqueue()`: Transition from *Created* to *Queued*
- `workerpicksup()`: Transition from *Queued* to *Processing*
- `checkintegrity()`: Transition from *Processing* to *Validating*
- `validationpassed()`: Transition from *Validating* to *Extracting*
- `validationerror()`: Transition from *Validating* to *Failed*
- `extractionsuccess()`: Transition from *Extracting* to *Completed*
- `extractionerror()`: Transition from *Extracting* to *Failed*
- `retryjob()`: Transition from *Failed* to *Queued*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### IngestController

**Type**: passive_class

API endpoint untuk menerima data.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ControllerID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### IngestService

**Type**: passive_class

Service untuk memvalidasi dan memproses data yang diingest.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ServiceID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### MessageQueue

**Type**: passive_class

Message queue untuk mengelola job.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `QueueID` | uuid | - |
| `QueueName` | string | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### ExtractionResult

**Type**: class

Hasil dari proses ekstraksi teks.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ResultID` | uuid | - |
| `JobID` | uuid | - |
| `ExtractedText` | string | - |
| `Metadata` | json | - |
| `Status` | state | - |

**Methods**:

- `startextraction()`: Transition from *Pending* to *Extracting*
- `extractioncomplete()`: Transition from *Extracting* to *TextExtracted*
- `validatecontent()`: Transition from *TextExtracted* to *Validating*
- `contentisvalid()`: Transition from *Validating* to *Valid*
- `contentisinvalid()`: Transition from *Validating* to *Invalid*
- `markasfailed()`: Transition from *Invalid* to *Failed*
- `addmetadata()`: Transition from *Valid* to *MetadataEnriched*
- `prepareforstorage()`: Transition from *MetadataEnriched* to *ReadyForStorage*
- `sendtostorage()`: Transition from *ReadyForStorage* to *Storing*
- `storagesuccess()`: Transition from *Storing* to *Stored*
- `storageerror()`: Transition from *Storing* to *StorageFailed*
- `retrystorage()`: Transition from *StorageFailed* to *Storing*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### ExtractionWorker

**Type**: passive_class

Worker yang memproses job ekstraksi.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `WorkerID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### ExtractionFactory

**Type**: passive_class

Factory untuk memilih strategy ekstraksi yang tepat.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `FactoryID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### PdfExtractor

**Type**: passive_class

Strategy untuk ekstraksi PDF.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ExtractorID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### OcrExtractor

**Type**: passive_class

Strategy untuk ekstraksi gambar dengan OCR.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ExtractorID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### AudioTranscriber

**Type**: passive_class

Strategy untuk transkripsi audio.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `TranscriberID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### StorageService

**Type**: passive_class

Service untuk menyimpan dokumen yang telah diekstrak.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ServiceID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### EmbeddingGenerator

**Type**: passive_class

Generator untuk membuat vector embedding dari teks.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `GeneratorID` | uuid | - |
| `ModelName` | string | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### VectorClient

**Type**: passive_class

Client untuk berinteraksi dengan vector database.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ClientID` | uuid | - |
| `DatabaseUrl` | string | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### MetadataClient

**Type**: passive_class

Client untuk menyimpan metadata dokumen.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ClientID` | uuid | - |
| `DatabaseUrl` | string | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Answer

**Type**: class

Jawaban yang dihasilkan oleh AI untuk query pengguna.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `AnswerID` | uuid | - |
| `QueryText` | string | - |
| `AnswerText` | string | - |
| `Sources` | json | - |
| `Confidence` | float | - |
| `Status` | state | - |

**Methods**:

- `searchrelevantdocs()`: Transition from *Received* to *RetrievingContext*
- `docsretrieved()`: Transition from *RetrievingContext* to *ContextFound*
- `nodocsfound()`: Transition from *RetrievingContext* to *NoContext*
- `prepareprompt()`: Transition from *ContextFound* to *BuildingPrompt*
- `usefallbackprompt()`: Transition from *NoContext* to *BuildingPrompt*
- `sendtollm()`: Transition from *BuildingPrompt* to *GeneratingAnswer*
- `startstreaming()`: Transition from *GeneratingAnswer* to *Streaming*
- `chunksreceived()`: Transition from *Streaming* to *PartialAnswer*
- `continuestreaming()`: Transition from *PartialAnswer* to *Streaming*
- `streamfinished()`: Transition from *PartialAnswer* to *Complete*
- `llmerror()`: Transition from *GeneratingAnswer* to *Failed*
- `retrywithfallback()`: Transition from *Failed* to *GeneratingAnswer*
- `maxretriesexceeded()`: Transition from *Failed* to *ErrorResponse*
- `formatanswer()`: Transition from *Complete* to *FormattingResponse*
- `formattingcomplete()`: Transition from *FormattingResponse* to *ReadyToSend*
- `delivertouser()`: Transition from *ReadyToSend* to *Sent*
- `senderrormessage()`: Transition from *ErrorResponse* to *Sent*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### QueryController

**Type**: passive_class

Controller untuk menangani query pengguna.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ControllerID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### RAGService

**Type**: passive_class

Service untuk mengorkestrasi proses RAG.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ServiceID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### DocumentRetriever

**Type**: passive_class

Retriever untuk mencari dokumen relevan.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `RetrieverID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### PromptBuilder

**Type**: passive_class

Builder untuk menyusun prompt RAG.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `BuilderID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### LLMClient

**Type**: passive_class

Client untuk berkomunikasi dengan Large Language Model.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ClientID` | uuid | - |
| `ModelName` | string | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Insight

**Type**: class

Insight yang dihasilkan dari analisis proaktif.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `InsightID` | uuid | - |
| `Title` | string | - |
| `Description` | string | - |
| `RelatedDocs` | json | - |
| `Priority` | string | - |
| `Score` | float | - |
| `UserID` | uuid | - |
| `Status` | state | - |

**Methods**:

- `foundconnections()`: Transition from *Analyzing* to *PatternDetected*
- `noinsightsfound()`: Transition from *Analyzing* to *NoPattern*
- `calculatepriority()`: Transition from *PatternDetected* to *Scoring*
- `scoreabovethreshold()`: Transition from *Scoring* to *HighPriority*
- `scorebelowthreshold()`: Transition from *Scoring* to *LowPriority*
- `checkrelevance()`: Transition from *HighPriority* to *Validating*
- `storeforlater()`: Transition from *LowPriority* to *Queued*
- `passesvalidation()`: Transition from *Validating* to *Valid*
- `notrelevant()`: Transition from *Validating* to *Invalid*
- `preparenotification()`: Transition from *Valid* to *ReadyToNotify*
- `discardinsight()`: Transition from *Invalid* to *Discarded*
- `sendtouser()`: Transition from *ReadyToNotify* to *Notifying*
- `deliverysuccess()`: Transition from *Notifying* to *Sent*
- `deliveryfailed()`: Transition from *Notifying* to *Failed*
- `retry()`: Transition from *Failed* to *Notifying*
- `maxretries()`: Transition from *Failed* to *Abandoned*
- `useropensnotification()`: Transition from *Sent* to *Viewed*
- `notviewedin7days()`: Transition from *Sent* to *Expired*
- `useracknowledges()`: Transition from *Viewed* to *Acknowledged*
- `userdismisses()`: Transition from *Viewed* to *Dismissed*
- `useractsoninsight()`: Transition from *Acknowledged* to *Actioned*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### ProactiveWorker

**Type**: passive_class

Worker yang menjalankan analisis proaktif terjadwal.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `WorkerID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### AnalysisEngine

**Type**: passive_class

Mesin yang menjalankan berbagai strategi analisis.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `EngineID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### NotificationService

**Type**: passive_class

Service untuk mengirim notifikasi insight ke pengguna.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `ServiceID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### IAnalysisStrategy

**Type**: passive_class

Interface untuk strategi analisis (e.g., ConnectionFinder).

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `StrategyID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### ConnectionFinder

**Type**: passive_class

Implementasi strategi untuk menemukan koneksi antar dokumen.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `FinderID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### GapDetector

**Type**: passive_class

Implementasi strategi untuk mendeteksi kesenjangan pengetahuan.

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `DetectorID` | uuid | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

---

## Relationships

### R1: Unknown ↔ Unknown

**Type**: association

ChatView menampilkan Message.

- **Unknown** [1]  ← **Unknown** [1] 

### R2: Unknown ↔ Unknown

**Type**: association

ChatView menggunakan ApiClient untuk komunikasi.

- **Unknown** [1]  ← **Unknown** [1] 

### R3: Unknown ↔ Unknown

**Type**: association

IngestController menggunakan IngestService.

- **Unknown** [1]  ← **Unknown** [1] 

### R4: Unknown ↔ Unknown

**Type**: association

IngestService membuat IngestionJob.

- **Unknown** [1]  ← **Unknown** [1] 

### R5: Unknown ↔ Unknown

**Type**: association

IngestionJob dipublikasikan ke MessageQueue.

- **Unknown** [1]  ← **Unknown** [1] 

### R6: Unknown ↔ Unknown

**Type**: association

ExtractionWorker menggunakan ExtractionFactory.

- **Unknown** [1]  ← **Unknown** [1] 

### R7: Unknown ↔ Unknown

**Type**: association

ExtractionWorker membuat ExtractionResult.

- **Unknown** [1]  ← **Unknown** [1] 

### R8: Unknown ↔ Unknown

**Type**: association

ExtractionFactory mengelola berbagai extractor strategies.

- **Unknown** [1]  ← **Unknown** [1] 

### R9: Unknown ↔ Unknown

**Type**: association

StorageService menggunakan EmbeddingGenerator.

- **Unknown** [1]  ← **Unknown** [1] 

### R10: Unknown ↔ Unknown

**Type**: association

StorageService menggunakan VectorClient.

- **Unknown** [1]  ← **Unknown** [1] 

### R11: Unknown ↔ Unknown

**Type**: association

StorageService menggunakan MetadataClient.

- **Unknown** [1]  ← **Unknown** [1] 

### R12: Unknown ↔ Unknown

**Type**: association

QueryController menggunakan RAGService.

- **Unknown** [1]  ← **Unknown** [1] 

### R13: Unknown ↔ Unknown

**Type**: association

RAGService membuat Answer.

- **Unknown** [1]  ← **Unknown** [1] 

### R14: Unknown ↔ Unknown

**Type**: association

RAGService menggunakan DocumentRetriever.

- **Unknown** [1]  ← **Unknown** [1] 

### R15: Unknown ↔ Unknown

**Type**: association

RAGService menggunakan PromptBuilder.

- **Unknown** [1]  ← **Unknown** [1] 

### R16: Unknown ↔ Unknown

**Type**: association

RAGService menggunakan LLMClient.

- **Unknown** [1]  ← **Unknown** [1] 

### R17: Unknown ↔ Unknown

**Type**: association

ProactiveWorker menggunakan AnalysisEngine.

- **Unknown** [1]  ← **Unknown** [1] 

### R18: Unknown ↔ Unknown

**Type**: association

ProactiveWorker menggunakan NotificationService.

- **Unknown** [1]  ← **Unknown** [1] 

### R19: Unknown ↔ Unknown

**Type**: association

AnalysisEngine mengelola IAnalysisStrategy.

- **Unknown** [1]  ← **Unknown** [1] 

### R20: Unknown ↔ Unknown

**Type**: association

ConnectionFinder adalah implementasi dari IAnalysisStrategy.

- **Unknown** [1]  ← **Unknown** [1] 

### R21: Unknown ↔ Unknown

**Type**: association

GapDetector adalah implementasi dari IAnalysisStrategy.

- **Unknown** [1]  ← **Unknown** [1] 

### R22: Unknown ↔ Unknown

**Type**: association

AnalysisEngine menghasilkan Insight.

- **Unknown** [1]  ← **Unknown** [1] 

---

## State Machines

### Message State Machine

**Initial State**: Draft

**States**:

- **Draft**: No description
- **Sending**: No description
- **Sent**: No description
- **Delivered**: No description
- **Read**: No description
- **Failed**: No description

**State Transitions**:

```
Draft --[userClicksSend]--> Sending
Sending --[apiCallSuccess]--> Sent
Sending --[networkError]--> Failed
Failed --[retry]--> Sending
Sent --[serverConfirms]--> Delivered
Delivered --[userViews]--> Read
```

### IngestionJob State Machine

**Initial State**: Created

**States**:

- **Created**: No description
- **Queued**: No description
- **Processing**: No description
- **Validating**: No description
- **Extracting**: No description
- **Completed**: No description
- **Failed**: No description
- **Abandoned**: No description

**State Transitions**:

```
Created --[addToQueue]--> Queued
Queued --[workerPicksUp]--> Processing
Processing --[checkIntegrity]--> Validating
Validating --[validationPassed]--> Extracting
Validating --[validationError]--> Failed
Extracting --[extractionSuccess]--> Completed
Extracting --[extractionError]--> Failed
Failed --[retryJob]--> Queued
```

### ExtractionResult State Machine

**Initial State**: Pending

**States**:

- **Pending**: No description
- **Extracting**: No description
- **TextExtracted**: No description
- **Validating**: No description
- **Valid**: No description
- **Invalid**: No description
- **MetadataEnriched**: No description
- **ReadyForStorage**: No description
- **Storing**: No description
- **Stored**: No description
- **StorageFailed**: No description
- **Failed**: No description

**State Transitions**:

```
Pending --[startExtraction]--> Extracting
Extracting --[extractionComplete]--> TextExtracted
TextExtracted --[validateContent]--> Validating
Validating --[contentIsValid]--> Valid
Validating --[contentIsInvalid]--> Invalid
Invalid --[markAsFailed]--> Failed
Valid --[addMetadata]--> MetadataEnriched
MetadataEnriched --[prepareForStorage]--> ReadyForStorage
ReadyForStorage --[sendToStorage]--> Storing
Storing --[storageSuccess]--> Stored
Storing --[storageError]--> StorageFailed
StorageFailed --[retryStorage]--> Storing
```

### Answer State Machine

**Initial State**: Received

**States**:

- **Received**: No description
- **RetrievingContext**: No description
- **ContextFound**: No description
- **NoContext**: No description
- **BuildingPrompt**: No description
- **GeneratingAnswer**: No description
- **Streaming**: No description
- **PartialAnswer**: No description
- **Complete**: No description
- **FormattingResponse**: No description
- **ReadyToSend**: No description
- **Sent**: No description
- **Failed**: No description
- **ErrorResponse**: No description

**State Transitions**:

```
Received --[searchRelevantDocs]--> RetrievingContext
RetrievingContext --[docsRetrieved]--> ContextFound
RetrievingContext --[noDocsFound]--> NoContext
ContextFound --[preparePrompt]--> BuildingPrompt
NoContext --[useFallbackPrompt]--> BuildingPrompt
BuildingPrompt --[sendToLLM]--> GeneratingAnswer
GeneratingAnswer --[startStreaming]--> Streaming
Streaming --[chunksReceived]--> PartialAnswer
PartialAnswer --[continueStreaming]--> Streaming
PartialAnswer --[streamFinished]--> Complete
GeneratingAnswer --[llmError]--> Failed
Failed --[retryWithFallback]--> GeneratingAnswer
Failed --[maxRetriesExceeded]--> ErrorResponse
Complete --[formatAnswer]--> FormattingResponse
FormattingResponse --[formattingComplete]--> ReadyToSend
ReadyToSend --[deliverToUser]--> Sent
ErrorResponse --[sendErrorMessage]--> Sent
```

### Insight State Machine

**Initial State**: Analyzing

**States**:

- **Analyzing**: No description
- **PatternDetected**: No description
- **NoPattern**: No description
- **Scoring**: No description
- **HighPriority**: No description
- **LowPriority**: No description
- **Validating**: No description
- **Valid**: No description
- **Invalid**: No description
- **ReadyToNotify**: No description
- **Notifying**: No description
- **Sent**: No description
- **Failed**: No description
- **Abandoned**: No description
- **Viewed**: No description
- **Expired**: No description
- **Acknowledged**: No description
- **Dismissed**: No description
- **Actioned**: No description
- **Queued**: No description
- **Discarded**: No description

**State Transitions**:

```
Analyzing --[foundConnections]--> PatternDetected
Analyzing --[noInsightsFound]--> NoPattern
PatternDetected --[calculatePriority]--> Scoring
Scoring --[scoreAboveThreshold]--> HighPriority
Scoring --[scoreBelowThreshold]--> LowPriority
HighPriority --[checkRelevance]--> Validating
LowPriority --[storeForLater]--> Queued
Validating --[passesValidation]--> Valid
Validating --[notRelevant]--> Invalid
Valid --[prepareNotification]--> ReadyToNotify
Invalid --[discardInsight]--> Discarded
ReadyToNotify --[sendToUser]--> Notifying
Notifying --[deliverySuccess]--> Sent
Notifying --[deliveryFailed]--> Failed
Failed --[retry]--> Notifying
Failed --[maxRetries]--> Abandoned
Sent --[userOpensNotification]--> Viewed
Sent --[notViewedIn7Days]--> Expired
Viewed --[userAcknowledges]--> Acknowledged
Viewed --[userDismisses]--> Dismissed
Acknowledged --[userActsOnInsight]--> Actioned
```

---

## API Quick Reference

### Active Classes (with State Machines)

| Class | Initial State | Available Events |
|-------|---------------|------------------|
| **Message** | Draft | `retry`, `userClicksSend`, `apiCallSuccess` (+3 more) |
| **IngestionJob** | Created | `workerPicksUp`, `extractionSuccess`, `validationPassed` (+5 more) |
| **ExtractionResult** | Pending | `extractionComplete`, `storageSuccess`, `storageError` (+9 more) |
| **Answer** | Received | `preparePrompt`, `sendToLLM`, `useFallbackPrompt` (+14 more) |
| **Insight** | Analyzing | `userAcknowledges`, `maxRetries`, `checkRelevance` (+18 more) |

---

## Usage Examples

### Basic Usage

```python
from library import *

# Create Message instance
obj = Message()
print(obj.Status)

# Trigger event: userClicksSend
obj.userclickssend()
print(obj.Status)

# Validate and serialize
if obj.validate():
    data = obj.to_dict()
    print(data)
```
